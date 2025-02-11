# Debts_Management/models.py
from django.db import models
from django.utils import timezone

class CustomerDebt(models.Model):
    customer_name = models.CharField(max_length=255)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')
    
    def __str__(self):
        return f"Customer Debt - {self.customer_name} - {self.amount_due}"

class SupplierDebt(models.Model):
    supplier_name = models.CharField(max_length=255)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')

    def __str__(self):
        return f"Supplier Debt - {self.supplier_name} - {self.amount_due}"

class DebtPaymentTracking(models.Model):
    debt = models.ForeignKey(CustomerDebt, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    method = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Bank', 'Bank'), ('Online', 'Online')])
    
    def __str__(self):
        return f"Payment of {self.amount_paid} for {self.debt.customer_name}"

class OutstandingBalance(models.Model):
    debt = models.ForeignKey(CustomerDebt, on_delete=models.CASCADE, related_name='outstanding_balances')
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Outstanding Balance for {self.debt.customer_name}"

class DueDateReminder(models.Model):
    debt = models.ForeignKey(CustomerDebt, on_delete=models.CASCADE, related_name='due_date_reminders')
    reminder_date = models.DateField()
    reminder_method = models.CharField(max_length=50, choices=[('SMS', 'SMS'), ('Email', 'Email')])
    
    def __str__(self):
        return f"Reminder for {self.debt.customer_name} - {self.reminder_date}"

class DebtReport(models.Model):
    debt = models.ForeignKey(CustomerDebt, on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=50, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')])
    report_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return f"Report for {self.debt.customer_name} - {self.report_type}"
