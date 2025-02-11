from django.db import models
# from ai.lead_scoring import predict_lead_score
from users.models import CustomUser


class Customer(models.Model):
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    full_name = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lead_score = models.FloatField(default=0.0)  # AI-generated lead score
    
    def total_spent(self):
        return Order.objects.filter(customer=self).aggregate(total=models.Sum('total_amount'))['total'] or 0.00

    def order_count(self):
        return Order.objects.filter(customer=self).count()
    
    # def save(self, *args, **kwargs):
    #     self.lead_score = predict_lead_score(self)
    #     super().save(*args, **kwargs)
