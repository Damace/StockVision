from django.contrib import admin
from django.urls import path
from django.urls import include
from users.views import index
from users.views import user_login
from users.views import user_logout
from users.views import permission_redirect
from customers.views import customers_list
# from sales.views import orders_list
from users.views import dashboard

urlpatterns = [
    path('', index, name='index'),
    path('', include('inventory.urls')),
    path('', include('sales.urls')),
    path('', include('reports.urls')),
    path('', include('backup.urls')),
    path('', include("debt.urls")),
    path('', include("Purchases_Expenses.urls")),
    path("home/", user_login, name="home"),
    path('permission/<str:perm_name>/', permission_redirect, name='permission_redirect'),
    path("logout/", user_logout, name="logout"),
    path('admin/', admin.site.urls),
    path('customers/', include('customers.urls')),
    path('customers/', customers_list, name="customers_list"),
    # path('orders/', orders_list, name="orders_list"),
    path('dashboard/',dashboard, name='dashboard'),

]
