from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Sales Manager', 'Sales Manager'),
        ('Sales Rep', 'Sales Representative'),
        ('Customer', 'Customer'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Customer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    def __str__(self):
        return self.username
