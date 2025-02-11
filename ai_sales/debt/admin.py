from django.contrib import admin
from .models import SupplierDebt, CustomerDebt

@admin.register(SupplierDebt)
class SupplierDebtAdmin(admin.ModelAdmin):
    list_display = ("supplier", "amount", "due_date", "paid", "created_at")
    list_filter = ("paid", "due_date")
    search_fields = ("supplier",)

@admin.register(CustomerDebt)
class CustomerDebtAdmin(admin.ModelAdmin):
    list_display = ("customer", "amount", "due_date", "paid", "created_at")
    list_filter = ("paid", "due_date")
    search_fields = ("customer__username",)


from django.contrib import admin
from .models import Expenditure

admin.site.register(Expenditure)
