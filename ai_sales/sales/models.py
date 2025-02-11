from django.db import models
from customers.models import Customer
from inventory.models import Product
from django.db import models
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class NewSale(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Mobile Money', 'Mobile Money'),
        ('Bank Transfer', 'Bank Transfer'),
    ]

    customer = models.CharField(max_length=50, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    payment_status = models.CharField(
        max_length=50,
        choices=[('Paid', 'Paid'), ('Pending', 'Pending')],
        default='Paid'
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHODS,
        default='Cash'
    )
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure final amount calculation before saving
        self.total_amount = (self.price * self.quantity) - self.discount
        super(NewSale, self).save(*args, **kwargs)


@receiver(post_save, sender=NewSale)
def update_stock_on_sale(sender, instance, created, **kwargs):
    """Reduce stock quantity after a sale"""
    if created:  # Ensures stock reduction happens only on new sales
        product = instance.product
        if product.stock_quantity >= instance.quantity:
            product.stock_quantity -= instance.quantity
            product.save()
        else:
            raise ValueError("Not enough stock available for this sale.")

class Invoice(models.Model):
   
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    issued_date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    description = models.TextField()
    status = models.CharField(
        max_length=20, 
        choices=[('Pending', 'Pending'), ('Paid', 'Paid')],
        default='Pending'
    )

    def __str__(self):
        return f"Invoice #{self.id} - {self.student.full_name}"

class Receipt(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    receipt_date = models.DateField(default=timezone.now)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50)
    
    def __str__(self):
        return f"Receipt #{self.receipt_number} - Invoice #{self.invoice.id}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order {self.id} - {self.customer.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('Credit Card', 'Credit Card'),
        ('PayPal', 'PayPal'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash on Delivery', 'Cash on Delivery'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):
        return f"Payment for Order {self.order.id}"
    

class ReturnRefund(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    reason = models.TextField()
    refund_method = models.CharField(max_length=50, choices=[('credit', 'Credit to Account'), 
                                                             ('bank', 'Bank Transfer'),
                                                             ('cash', 'Cash Refund')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return/Refund for Order {self.order_number}"
