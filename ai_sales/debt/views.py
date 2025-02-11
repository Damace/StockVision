from django.shortcuts import render, redirect
from .models import SupplierDebt, CustomerDebt
from django.contrib.auth.decorators import login_required
from inventory.models import Product

# Supplier Debt View
@login_required
def supplier_debt_list(request):
    debts = SupplierDebt.objects.all()
    debts_all = SupplierDebt.objects.all().count
    product_all = Product.objects.all().count
    
    context = {
        "debts": debts,
        "debts_all": debts_all,   
        "product_all": product_all,  
    }
    
    return render(request, "debt/index.html", context)

@login_required
def my_debt_list(request):
    debts = SupplierDebt.objects.all()
    debts_all = SupplierDebt.objects.all().count
    product_all = Product.objects.all().count
    
    context = {
        "debts": debts,
        "debts_all": debts_all,   
        "product_all": product_all,  
    }
    
    return render(request, "debt/mydept.html", context)




@login_required
def add_supplier_debt(request):
    if request.method == "POST":
        supplier = request.POST["supplier"]
        amount = request.POST["amount"]
        due_date = request.POST["due_date"]
        description = request.POST.get("description", "")

        SupplierDebt.objects.create(
            supplier=supplier,
            amount=amount,
            due_date=due_date,
            description=description,
        )
        return redirect("supplier_debt_list")

    return render(request, "debt/add_supplier_debt.html")


# Customer Debt View
@login_required
def customer_debt_list(request):
    debts = CustomerDebt.objects.filter(customer=request.user)
    return render(request, "debt/customer_debt_list.html", {"debts": debts})

@login_required
def add_customer_debt(request):
    if request.method == "POST":
        amount = request.POST["amount"]
        due_date = request.POST["due_date"]
        description = request.POST.get("description", "")

        CustomerDebt.objects.create(
            customer=request.user,
            amount=amount,
            due_date=due_date,
            description=description,
        )
        return redirect("customer_debt_list")

    return render(request, "debt/add_customer_debt.html")
