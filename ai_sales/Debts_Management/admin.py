# Debts_Management/admin.py
from django.contrib import admin
from .models import CustomerDebt, SupplierDebt, DebtPaymentTracking, OutstandingBalance, DueDateReminder, DebtReport

# Register your models here
@admin.register(CustomerDebt)
class CustomerDebtAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'amount_due', 'due_date', 'status')
    list_filter = ('status', 'due_date')
    search_fields = ('customer_name', 'amount_due')

@admin.register(SupplierDebt)
class SupplierDebtAdmin(admin.ModelAdmin):
    list_display = ('supplier_name', 'amount_due', 'due_date', 'status')
    list_filter = ('status', 'due_date')
    search_fields = ('supplier_name', 'amount_due')

# @admin.register(DebtPaymentTracking)
class DebtPaymentTrackingAdmin(admin.ModelAdmin):
    list_display = ('debt', 'amount_paid', 'payment_date', 'method')
    list_filter = ('payment_date', 'method')
    search_fields = ('debt__customer_name', 'amount_paid')

@admin.register(OutstandingBalance)
class OutstandingBalanceAdmin(admin.ModelAdmin):
    list_display = ('debt', 'balance_amount')
    list_filter = ('debt__customer_name',)

@admin.register(DueDateReminder)
class DueDateReminderAdmin(admin.ModelAdmin):
    list_display = ('debt', 'reminder_date', 'reminder_method')
    list_filter = ('reminder_date', 'reminder_method')
    search_fields = ('debt__customer_name',)

@admin.register(DebtReport)
class DebtReportAdmin(admin.ModelAdmin):
    list_display = ('debt', 'report_type', 'report_date')
    list_filter = ('report_date', 'report_type')
    search_fields = ('debt__customer_name',)
