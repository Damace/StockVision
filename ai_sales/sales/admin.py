from django.contrib import admin
from .models import Order, OrderItem, Payment

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'customer', 'order_date', 'status')
#     list_filter = ('status', 'order_date')
#     search_fields = ('customer__user__username', 'customer__user__email')

# # @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ('order', 'product', 'quantity', 'price')
#     list_filter = ('order__order_date', 'product')
#     search_fields = ('product__name', 'order__customer__user__username')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'payment_method', 'payment_date', 'status')
    list_filter = ('payment_method', 'status', 'payment_date')
    search_fields = ('order__customer__user__username', 'order__id')



from django.contrib import admin
from .models import NewSale, Invoice, Receipt, Order, OrderItem, Payment, ReturnRefund

# Registering NewSale model
@admin.register(NewSale)
class NewSaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer','product','quantity', 'price', 'discount', 'total_amount','payment_method','payment_status', 'date')
    search_fields = ('customer__name', 'payment_status')
    list_filter = ('payment_status', 'date')

# # Registering Invoice model
# # @admin.register(Invoice)
# class InvoiceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'customer', 'issued_date', 'amount', 'due_date', 'status')
#     search_fields = ('customer__name', 'status')
#     list_filter = ('status', 'issued_date')

# # Registering Receipt model
# # @admin.register(Receipt)
# class ReceiptAdmin(admin.ModelAdmin):
#     list_display = ('id', 'invoice', 'receipt_number', 'amount_paid', 'payment_method', 'receipt_date')
#     search_fields = ('invoice__id', 'receipt_number', 'payment_method')
#     list_filter = ('payment_method', 'receipt_date')


# # Registering ReturnRefund model
# # @admin.register(ReturnRefund)
# class ReturnRefundAdmin(admin.ModelAdmin):
#     list_display = ('id', 'customer', 'reason', 'refund_method', 'created_at')
#     search_fields = ('customer__name', 'refund_method')
#     list_filter = ('refund_method', 'created_at')

