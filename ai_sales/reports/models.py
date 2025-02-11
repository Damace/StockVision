# In your Django models.py
from django.db import models

class CompanyProfile(models.Model):
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.company_name
