from django.urls import path
from . import views

urlpatterns = [
    # Supplier Debt URLs
    path("supplier/", views.supplier_debt_list, name="supplier_debt_list"),
     path("my_debt_list/", views.my_debt_list, name="my_debt_list"),
    path("supplier/add/", views.add_supplier_debt, name="add_supplier_debt"),

    # Customer Debt URLs
    path("customer/", views.customer_debt_list, name="customer_debt_list"),
    path("customer/add/", views.add_customer_debt, name="add_customer_debt"),
]


