from django.db import models
from enum import Enum
from django.utils import timezone


class StorageUnit(models.Model):
    name = models.CharField(max_length=50, unique=True, null=True)
    responsible = models.CharField(max_length=50, unique=True, null=True)
    is_active = models.BooleanField(null=True, verbose_name='Is active?')
    activation_date = models.DateTimeField(auto_now_add=False, null=True,
                                           verbose_name='Storage Unit Activation Date')
    closure_date = models.DateTimeField(auto_now_add=False, null=True, blank=True,
                                        verbose_name='Storage Unit Closure Date')

    class Meta:
        verbose_name = 'Storage Unit'
        verbose_name_plural = 'Storage Units'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self.closure_date and timezone.now() > self.closure_date:
            self.is_active = False
        super().save(*args, **kwargs)


class CategoryEnum(Enum):
    TOOLS = 'Tools'
    MASTS = 'Masts'
    BATTERIES = 'Batteries'
    ACCESSORIES = 'Accessories'
    CABLES = 'Cables'
    ANTENNAS = 'Antennas'
    NUTS_AND_BOLTS = 'Nuts and Bolts'
    CONNECTORS_PINS_BUS_BARS = 'Connectors, Pins, and Bus Bars'
    SENSORS = 'Sensors'
    BOARDS_AND_ELECTRONICS = 'Boards and Electronics'
    SUPPORTS = 'Supports'
    OTHERS = 'Others'


class Material(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=50,
        choices=[(cat.name, cat.value) for cat in CategoryEnum],
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Material Registration'
        verbose_name_plural = 'Material Registrations'

    def __str__(self):
        return self.name


class StockLevel(Enum):
    NORMAL = 'normal'
    CRITICAL = 'critical'
    ZERO = 'zero'

    @classmethod
    def choices(cls):
        return [(choice.value, choice.name) for choice in cls]


class MaterialQuantityPerUnit(models.Model):
    unit = models.ForeignKey(StorageUnit, on_delete=models.PROTECT)
    material = models.ForeignKey(Material, on_delete=models.PROTECT)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    minimum = models.PositiveIntegerField(default=5)
    stock_level = models.CharField(
        max_length=20,
        choices=StockLevel.choices()
    )

    def get_stock_level(self):
        if self.quantity_in_stock == 0:
            return StockLevel.ZERO
        elif self.quantity_in_stock <= self.minimum:
            return StockLevel.CRITICAL
        else:
            return StockLevel.NORMAL

    def save(self, *args, **kwargs):
        self.stock_level = self.get_stock_level().value
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Materials in Stock'

    def __str__(self):
        return f' Material {self.material} / Quantidade {self.quantity_in_stock}'


class Package(models.Model):
    name = models.CharField(max_length=100)
    materials = models.ManyToManyField(Material, through='PackageItems')

    def __str__(self):
        return self.name


class PackageItems(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name="Package")
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='Material')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return 'Item:'


class MaterialEntry(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    entry_date = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=100, null=True)
    destination = models.ForeignKey(StorageUnit, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'External - Material Entry'
        verbose_name_plural = 'External - Material Entries'

    def __str__(self):
        return f"Material Entry - {self.material}"


class ServiceTypeEnum(Enum):
    INSTALLATION = 'Installation'
    PREVENTIVE_MAINTENANCE = 'Preventive Maintenance'
    CORRECTIVE_MAINTENANCE = 'Corrective Maintenance'

    @classmethod
    def choices(cls):
        return [(type.value, type.value) for type in cls]


class MaterialExit(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    exit_date = models.DateTimeField(auto_now_add=True)
    debit_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE, null=True)
    destination = models.CharField(max_length=100, null=True)  # mudar Para farm
    service = models.CharField(max_length=100, choices=ServiceTypeEnum.choices())

    class Meta:
        verbose_name = 'External - Material Exit'
        verbose_name_plural = 'External - Material Exits'

    def __str__(self):
        return f"Material Exit from Package: {self.package} With destination to: {self.destination} - " \
               f"Debited from unit: {self.debit_unit}"


class InternalTransfer(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    exit_date = models.DateTimeField(auto_now_add=True, verbose_name='Date of departure from the sending unit')
    debit_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE, null=True, related_name="debit_transfer")
    credit_unit = models.ForeignKey(StorageUnit, on_delete=models.CASCADE, null=True, related_name="credit_transfer")
    entry_date = models.DateTimeField(auto_now_add=False, blank=True, null=True,
                                      verbose_name='Date of entry at the destination unit')
    delivered = models.BooleanField(null=True, verbose_name='Was it delivered to the destination unit?')
    comments = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Internal Material Transfer'
        verbose_name_plural = 'Internal Material Transfers'

    def __str__(self):
        return f"Internal Transfer from Package: {self.package} With destination to: {self.credit_unit} - " \
               f"Debited from unit: {self.debit_unit}"

    def save(self, *args, **kwargs):
        if self.entry_date:
            self.delivered = True
        else:
            self.delivered = False
        super().save(*args, **kwargs)
