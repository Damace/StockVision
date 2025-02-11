from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=1)
    max_stock = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    supplier = models.CharField(max_length=255,blank=True)
    
    def save(self, *args, **kwargs):
        # Automatically update max_stock when stock_quantity changes
        if self.stock_quantity > 0:
            self.max_stock = self.stock_quantity*2 # Example: max_stock is twice the stock_quantity
        else:
            self.max_stock = 100  # Set a default max_stock when stock_quantity is zero or not provided
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name


from django.db import models

class StockAdjustment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_adjusted = models.IntegerField()
    adjustment_reason = models.TextField()
    adjustment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adjustment for {self.product.name}"

class StockTransfer(models.Model):
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_transferred = models.IntegerField()
    transfer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transfer of {self.product.name}"

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name

class LowStockAlert(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    threshold_quantity = models.PositiveIntegerField()
    alert_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Low stock alert for {self.product.name}"

class ExpiryManagement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    expiry_date = models.DateField()

    def __str__(self):
        return f"Expiry date for {self.product.name}"


from django.db import models 
from inventory.models import Product 

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="purchases")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="purchases")
    purchase_date = models.DateField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # In percentage
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Completed", "Completed"), ("Cancelled", "Cancelled")],
        default="Pending"
    )

    debt_status = models.CharField(
        max_length=20,
        choices=[("Paid", "Paid"), ("Unpaid", "Unpaid"), ("Partially Paid", "Partially Paid")],
        default="Unpaid"
    )

    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance_due = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calculate total price with discount
        discount_amount = (self.unit_price * self.quantity) * (self.discount / 100)
        self.total_price = (self.unit_price * self.quantity) - discount_amount

        # Calculate balance due
        self.balance_due = self.total_price - self.amount_paid

        # Update debt status
        if self.balance_due == 0:
            self.debt_status = "Paid"
        elif self.amount_paid > 0 and self.balance_due > 0:
            self.debt_status = "Partially Paid"
        else:
            self.debt_status = "Unpaid"

        super(Purchase, self).save(*args, **kwargs)

    def __str__(self):
        return f"Purchase {self.id} - {self.supplier.name} - {self.product.name} - {self.debt_status}"


from django.db import models

class Cargo(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partially_paid', 'Partially Paid'),
        ('fully_paid', 'Fully Paid'),
    ]

    cargo_name = models.CharField(max_length=255)
    importer_name = models.CharField(max_length=255)
    arrival_date = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance_due = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    storage_location = models.CharField(max_length=255, blank=True, null=True)
    release_status = models.BooleanField(default=False)  # True if released, False if still held
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """Automatically calculate the balance due and update the payment status."""
        self.balance_due = self.total_cost - self.amount_paid
        if self.balance_due <= 0:
            self.payment_status = 'fully_paid'
        elif self.amount_paid > 0:
            self.payment_status = 'partially_paid'
        else:
            self.payment_status = 'pending'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cargo_name} - {self.importer_name}"
