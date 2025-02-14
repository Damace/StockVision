# admin.py
from django.contrib import admin
from .models import CompanyProfile

class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'phone_number', 'email', 'address')
    search_fields = ('company_name', 'phone_number', 'email')
    list_filter = ('company_name',)

# Register the model with the admin site
# admin.site.register(CompanyProfile, CompanyProfileAdmin)
