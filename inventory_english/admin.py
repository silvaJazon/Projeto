from django.contrib import admin
from django import forms
from .models import Material, Package, PackageItems, MaterialExit, MaterialEntry, StorageUnit, \
    MaterialQuantityPerUnit, InternalTransfer


@admin.register(MaterialQuantityPerUnit)
class MaterialQuantityPerUnitAdmin(admin.ModelAdmin):
    list_display = ['unit', 'material', 'quantity_in_stock']
    list_filter = ['unit', 'material']
    ordering = ['material']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class QuantityUnitInline(admin.TabularInline):
    model = MaterialQuantityPerUnit
    extra = 0
    readonly_fields = ['unit', 'material', 'quantity_in_stock']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(StorageUnit)
class StorageUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'responsible', 'is_active', 'activation_date', 'closure_date']


class PackageItemsInline(admin.TabularInline):
    model = PackageItems


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    inlines = [PackageItemsInline]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    ordering = ['name']
    list_filter = ['category']


class MaterialEntryAdminForm(forms.ModelForm):
    class Meta:
        model = MaterialEntry
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        credit_unit_active = cleaned_data.get('destination').is_active

        if not credit_unit_active:
            msg = "The credit unit is inactive!"
            self.add_error('destination', msg)


@admin.register(MaterialEntry)
class MaterialEntryAdmin(admin.ModelAdmin):
    list_display = ['material', 'quantity', 'entry_date', 'sender', 'destination']
    form = MaterialEntryAdminForm
    list_filter = ['material__category', 'entry_date', 'sender']

    def save_model(self, request, obj, form, change):
        material = obj.material
        entry_quantity = obj.quantity
        destination_unit = obj.destination

        if destination_unit:
            # Add entry quantity to material stock for the destination unit #
            quantity_unit, created = MaterialQuantityPerUnit.objects.get_or_create(unit=destination_unit,
                                                                                   material=material)

            if not quantity_unit.quantity_in_stock:
                quantity_unit.quantity_in_stock = 0

            quantity_unit.quantity_in_stock += entry_quantity
            quantity_unit.save()

        super().save_model(request, obj, form, change)


class MaterialExitAdminForm(forms.ModelForm):
    class Meta:
        model = MaterialExit
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        package = cleaned_data.get('package')
        debit_unit = cleaned_data.get('debit_unit')
        debit_unit_active = cleaned_data.get('debit_unit').is_active if debit_unit else False

        for item in package.packageitems_set.all():
            material = item.material
            exit_quantity = item.quantity

            try:
                quantity_unit = MaterialQuantityPerUnit.objects.get(unit=debit_unit, material=material)
            except MaterialQuantityPerUnit.DoesNotExist:
                # Exception handling if the material does not exist in the debit unit
                msg = f"Material {material.name} does not exist in the debit unit {debit_unit.name}."
                self.add_error(None, msg)
                break

            if quantity_unit and quantity_unit.quantity_in_stock < exit_quantity:
                # Check if the stock quantity is sufficient for the exit
                msg = f"Insufficient stock quantity for {material.name} in the debit unit."
                self.add_error(None, msg)

        if not debit_unit_active:
            msg = "The debit unit is inactive!"
            self.add_error('debit_unit', msg)


@admin.register(MaterialExit)
class MaterialExitAdmin(admin.ModelAdmin):
    list_display = ['package', 'exit_date', 'destination', 'service', 'debit_unit']
    form = MaterialExitAdminForm

    def save_model(self, request, obj, form, change):
        package = obj.package
        debit_unit = obj.debit_unit
        successful_transaction = True

        for item in package.packageitems_set.all():
            material = item.material
            exit_quantity = item.quantity

            try:
                quantity_unit = MaterialQuantityPerUnit.objects.get(unit=debit_unit, material=material)
            except MaterialQuantityPerUnit.DoesNotExist:
                # Exception handling if the material does not exist in the debit unit
                msg = f"Material {material.name} does not exist in the debit unit {debit_unit.name}."
                form.add_error(None, msg)
                successful_transaction = False
                break

            if quantity_unit and quantity_unit.quantity_in_stock >= exit_quantity:
                # If the stock quantity is sufficient, update the stock
                quantity_unit.quantity_in_stock -= exit_quantity
                quantity_unit.save()
            elif quantity_unit:
                # Check if the stock quantity is insufficient
                msg = f"Insufficient stock quantity for {material.name} in the debit unit."
                form.add_error(None, msg)
                successful_transaction = False
                break
            else:
                # Exception handling if it's not possible to obtain the quantity
                msg = f"Error obtaining quantity for {material.name} in the debit unit {debit_unit.name}."
                form.add_error(None, msg)
                successful_transaction = False
                break

        if successful_transaction:
            super().save_model(request, obj, form, change)
        else:
            form.add_error(None, "The exit transaction was not completed successfully.")


class InternalTransferAdminForm(forms.ModelForm):
    class Meta:
        model = InternalTransfer
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        debit_unit = cleaned_data.get('debit_unit')
        credit_unit = cleaned_data.get('credit_unit')
        debit_unit_active = debit_unit.is_active if debit_unit else False
        credit_unit_active = credit_unit.is_active if credit_unit else False

        if debit_unit == credit_unit:
            msg = "Debit unit and credit unit must be different."
            self.add_error('credit_unit', msg)

        if not debit_unit_active:
            msg = "The debit unit is inactive!"
            self.add_error('debit_unit', msg)

        if not credit_unit_active:
            msg = "The credit unit is inactive!"
            self.add_error('credit_unit', msg)

        for item in cleaned_data.get('package').packageitems_set.all():
            material = item.material
            transferred_quantity = item.quantity

            try:
                quantity_debit_unit = MaterialQuantityPerUnit.objects.get(unit=debit_unit, material=material)
                quantity_credit_unit = MaterialQuantityPerUnit.objects.get(unit=credit_unit, material=material)
            except MaterialQuantityPerUnit.DoesNotExist:
                msg = f"Material {material.name} does not exist in one of the units."
                self.add_error(None, msg)
                break

            if quantity_debit_unit.quantity_in_stock < transferred_quantity:
                msg = f"Insufficient stock quantity for {material.name} in the debit unit."
                self.add_error(None, msg)
                break

        return cleaned_data


@admin.register(InternalTransfer)
class InternalTransferAdmin(admin.ModelAdmin):
    list_display = ['package', 'exit_date', 'debit_unit', 'credit_unit', 'entry_date', 'delivered']
    form = InternalTransferAdminForm

    def save_model(self, request, obj, form, change):
        debit_unit = obj.debit_unit
        credit_unit = obj.credit_unit
        successful_transaction = True

        for item in obj.package.packageitems_set.all():
            material = item.material
            transferred_quantity = item.quantity

            try:
                quantity_debit_unit = MaterialQuantityPerUnit.objects.get(unit=debit_unit, material=material)
                quantity_credit_unit = MaterialQuantityPerUnit.objects.get(unit=credit_unit,
                                                                           material=material)
            except MaterialQuantityPerUnit.DoesNotExist:
                msg = f"Material {material.name} does not exist in one of the units."
                form.add_error(None, msg)
                successful_transaction = False
                break

            if quantity_debit_unit.quantity_in_stock < transferred_quantity:
                msg = f"Insufficient stock quantity for {material.name} in the debit unit."
                form.add_error(None, msg)
                successful_transaction = False
                break

            if obj.delivered:
                quantity_debit_unit.quantity_in_stock -= transferred_quantity
                quantity_debit_unit.save()

                quantity_credit_unit.quantity_in_stock += transferred_quantity
                quantity_credit_unit.save()

        if successful_transaction:
            super().save_model(request, obj, form, change)
        else:
            form.add_error(None, "The internal transfer transaction was not completed successfully.")
