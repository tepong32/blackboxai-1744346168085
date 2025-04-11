from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'middle_initial', 
                   'is_staff', 'is_active', 'storage_quota_display')
    list_filter = ('is_staff', 'is_active')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'middle_initial', 'email')}),
        ('Storage', {'fields': ('storage_quota', 'used_storage')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'middle_initial', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    def storage_quota_display(self, obj):
        """Display storage quota in human-readable format"""
        quota_gb = obj.storage_quota / (1024 * 1024 * 1024)
        used_gb = obj.used_storage / (1024 * 1024 * 1024)
        return f'{used_gb:.2f}GB / {quota_gb:.2f}GB'
    storage_quota_display.short_description = 'Storage Usage'
