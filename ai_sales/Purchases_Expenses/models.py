# Purchases_Expenses/models.py
from django.db import models

# Model for Purchase
class Purchase(models.Model):
    supplier = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product_name} from {self.supplier}'

# Model for Supplier Payments
class SupplierPayment(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)
    
    def __str__(self):
        return f'Payment for {self.purchase.product_name} on {self.payment_date}'

# Model for Expense
class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    

    def __str__(self):
        return f'{self.description} - {self.amount}'

# Model for Purchase History
class PurchaseHistory(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    update_date = models.DateField()

    def __str__(self):
        return f'{self.purchase.product_name} - {self.status}'
