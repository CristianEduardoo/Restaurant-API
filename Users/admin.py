from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password  # Importar para encriptar contraseñas
from .models import User

# Desregistrar el modelo Group
admin.site.unregister(Group)

# Registramos el modelo User
# @admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "phone"]
    search_fields = ["email", "username"]

    # Sobrescribir el método para usar email como campo de identificación
    def get_fieldsets(self, request, obj=None):
        return (
            (None, {'fields': ('email', 'password')}),
            ('Información personal', {'fields': ('username', 'phone', 'date_joined')}),
            ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        )

    # Contraseña hasheada antes de guardar
    def save_model(self, request, obj, form, change):
        if form.cleaned_data["password"]:
            obj.password = make_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)
