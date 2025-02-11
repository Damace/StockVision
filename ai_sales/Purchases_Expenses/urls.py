# Purchases_Expenses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('purchases/', views.purchase_list, name='purchase_list'),
    path('supplier-payments/', views.supplier_payment_list, name='supplier_payment_list'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('purchase-history/', views.purchase_history_list, name='purchase_history_list'),
]
