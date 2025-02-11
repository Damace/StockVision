from django.contrib import admin
from .models import Product
from .models import Product, StockAdjustment, StockTransfer, Supplier, LowStockAlert, ExpiryManagement
from django.utils.html import format_html
from .models import Category
from .models import Cargo

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','category','selling_price', 'stock_quantity', 'created_at')
    exclude = ('max_stock',) 
    list_filter = ('stock_quantity', 'created_at')
    search_fields = ('name', 'stock_quantity')


# Stock Adjustment Admin
class StockAdjustmentAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_adjusted', 'adjustment_reason', 'adjustment_date')
    list_filter = ('adjustment_date', 'product')
    search_fields = ('product__name', 'adjustment_reason')
    ordering = ('-adjustment_date',)


# Stock Transfer Admin
class StockTransferAdmin(admin.ModelAdmin):
    list_display = ('product', 'from_location', 'to_location', 'quantity_transferred', 'transfer_date')
    list_filter = ('transfer_date', 'from_location', 'to_location')
    search_fields = ('product__name', 'from_location', 'to_location')
    ordering = ('-transfer_date',)


# Supplier Admin
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'phone_number', 'address')
    search_fields = ('name', 'contact_email')
    list_filter = ('name',)
    ordering = ('name',)


# Low Stock Alert Admin
class LowStockAlertAdmin(admin.ModelAdmin):
    list_display = ('product', 'threshold_quantity', 'alert_sent')
    list_filter = ('alert_sent', 'product')
    search_fields = ('product__name',)
    ordering = ('product',)


# Expiry Management Admin
class ExpiryManagementAdmin(admin.ModelAdmin):
    list_display = ('product', 'expiry_date')
    list_filter = ('expiry_date',)
    search_fields = ('product__name',)
    ordering = ('expiry_date',)
    
    
class CargoAdmin(admin.ModelAdmin):
    list_display = ('cargo_name', 'importer_name', 'arrival_date', 'total_cost', 'amount_paid', 'balance_due', 'payment_status', 'release_status')
    list_filter = ('payment_status', 'release_status', 'arrival_date')
    search_fields = ('cargo_name', 'importer_name')

admin.site.register(Cargo, CargoAdmin)
admin.site.register(StockAdjustment, StockAdjustmentAdmin)
admin.site.register(StockTransfer, StockTransferAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(LowStockAlert, LowStockAlertAdmin)
admin.site.register(ExpiryManagement, ExpiryManagementAdmin)
