from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'city', 'country', 'created_at')
    list_filter = ('city', 'country', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
