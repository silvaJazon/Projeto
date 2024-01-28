from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from usuarios.models import Usuario


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(Usuario, UserAdmin)