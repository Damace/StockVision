from django.shortcuts import render
from inventory.models import Product
from django.http import JsonResponse
from inventory.models import Supplier
from sales.models import NewSale

from .models import Purchase, SupplierPayment, Expense, PurchaseHistory

def purchase_list(request):
    purchases = Purchase.objects.all()
    return render(request, 'expenses/index.html', {'purchases': purchases})

def supplier_payment_list(request):
    payments = SupplierPayment.objects.all()
    return render(request, 'Purchases_Expenses/supplier_payment_list.html', {'payments': payments})


def expense_list(request):
    expenses = Expense.objects.all()
    total_expenses = Expense.objects.all()
    products = Product.objects.all() 
    expenses_all = Expense.objects.all().count()
    products_list = Product.objects.all().count()
    total_sales = NewSale.objects.all().count()
    
    
    
    
    context = {
        "expenses":expenses,
        "products": products,
        "products_list": products_list,
        "expenses_all":expenses_all,
        "total_sales": total_sales,
        "total_expenses": total_expenses,
        }
    
    return render(request, 'expenses/index.html',context)




def purchase_history_list(request):
    histories = PurchaseHistory.objects.all()
    return render(request, 'Purchases_Expenses/purchase_history_list.html', {'histories': histories})
