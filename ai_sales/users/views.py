from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout

def index(request):
    return render(request, 'users/index.html')  # Adjust path if necessary
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            context = {
            'username': username
            }
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")
            
    return redirect("index") 



def user_logout(request):
    username = request.user.username if request.user.is_authenticated else "Guest"
    logout(request)
    messages.success(request, "See you soon, {username}! You're always welcome back.")
    return render(request, "users/index.html")


def dashboard(request):
    return render(request, "home/index.html", {
        "username": request.user.username  
    })


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

