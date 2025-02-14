# Purchases_Expenses/admin.py
from django.contrib import admin
from .models import Purchase, SupplierPayment, Expense, PurchaseHistory

# Define the admin classes for each model to customize their display in the admin panel
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'supplier', 'quantity', 'price_per_unit', 'total_price', 'purchase_date')
    search_fields = ('product_name', 'supplier')
    list_filter = ('purchase_date', 'supplier')

class SupplierPaymentAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'payment_date', 'amount_paid', 'payment_method')
    search_fields = ('purchase__product_name', 'payment_method')
    list_filter = ('payment_date', 'payment_method')

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'date')
    search_fields = ('description',)
    list_filter = ('date',)

class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'status', 'update_date')
    search_fields = ('purchase__product_name', 'status')
    list_filter = ('update_date', 'status')

# Register your models with the corresponding admin classes
# admin.site.register(Purchase, PurchaseAdmin)
# admin.site.register(SupplierPayment, SupplierPaymentAdmin)
# admin.site.register(Expense, ExpenseAdmin)
# admin.site.register(PurchaseHistory, PurchaseHistoryAdmin)
