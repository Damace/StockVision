from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from sales.models import Order
from sales.models import NewSale
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from inventory.models import Product,Supplier
from debt.models import SupplierDebt,CustomerDebt

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import urllib
import base64
from django.shortcuts import render
from inventory.models import Product




def index(request):
    return render(request, 'users/index.html')  # Adjust path if necessar


def user_login(request):
    if request.method == "POST" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': 'success',
                'redirect_url': '/dashboard/',  # Redirect URL after successful login
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid username or password. Please try again.',
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request.',
    }, status=400)




def user_logout(request):
    username = request.user.username if request.user.is_authenticated else "Guest"
    logout(request)
    messages.success(request, "See you soon, {username}! You're always welcome back.")
    return render(request, "users/index.html")


def dashboard(request):
    products = Product.objects.all()
    df = pd.DataFrame(list(products.values("product_name", "stock_quantity")))
    plt.figure(figsize=(7, 5))
    sns.barplot(x="stock_quantity", y="product_name", data=df, palette="coolwarm")
    plt.xlabel("Stock Quantity", fontsize=10, fontweight="bold", color="darkblue")
    plt.ylabel("Product Name", fontsize=10, fontweight="bold", color="darkblue")
   
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
        
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    
    products = Product.objects.all() 
    products_list = Product.objects.all().count()
    total_sales =  NewSale.objects.all().count()
    debt_supplier = SupplierDebt.objects.all().count()
    debt_custer = CustomerDebt.objects.all().count()
    supplier_list = Supplier.objects.all().count()
    
    total_debts = debt_supplier +  debt_custer
    
    context = {
        "username": request.user.username,
        "products_list": products_list,
        "total_sales": total_sales,
        "total_debts" :total_debts,
        "supplier_list":supplier_list,
        "chart": image_base64,
        
        }
     
    return render(request, "home/index.html",context)


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def permission_redirect(request, perm_name):
    """ Redirect users based on their permissions. """
    permission_routes = {
        "customers.view_customer": "customers_list",
        "orders.view_order": "orders_list",
        "sales.view_sales": "sales_dashboard",
        "users.view_customuser":"customers_list",
    }

    # Get URL name from permission map
    url_name = permission_routes.get(perm_name, "home")  # Default to home if no match

    return redirect(url_name)

