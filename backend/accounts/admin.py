from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_analyst', 'is_manager')
    list_filter = ('is_staff', 'is_superuser', 'is_analyst', 'is_manager')
    fieldsets = UserAdmin.fieldsets + (
        ('Funções Específicas', {'fields': ('is_analyst', 'is_manager')}),
    )