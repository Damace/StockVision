from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    
    site_header = 'My Custom Admin Header'
    site_title = 'My Custom Admin Title'
    index_title = 'Welcome to My Custom Admin Dashboard'

    model = CustomUser
    list_display = ('username', 'email', 'role', 'phone', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('role', 'phone', 'profile_picture')}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('role', 'phone', 'profile_picture')}),)

admin.site.register(CustomUser, CustomUserAdmin)
