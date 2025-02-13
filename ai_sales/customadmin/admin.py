from django.contrib.admin import AdminSite
from django.contrib import admin
from sales.models import NewSale, Invoice, Receipt, Order, OrderItem, Payment, ReturnRefund

class CustomAdminSite(AdminSite):
    site_header = "Custom Admin Dashboard"
    site_title = "Admin Panel"
    index_title = "Welcome to Custom Admin"

custom_admin_site = CustomAdminSite(name="customadmin")

