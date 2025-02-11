from django.urls import path
from . import views
from django.urls import path
from .views import sales_list
from .views import new_sales
from . import views
from .views import new_sales, get_product_price
from .views import save_sale
from .views import add_sale
from .views import sales_trends_chart
from .views import sales_report
from .views import sales_reports

urlpatterns = [
    path('all_sales/', sales_list, name='all_sales'),
    path('create_sale/', views.create_sale, name='create_sale'),
    path('new_sales/', views.new_sales, name='new_sales'),
    path("new-sales/", new_sales, name="new-sales"),
    path("get-product-price/", get_product_price, name="get-product-price"),
    path("save-sale/", save_sale, name="save-sale"),
    path("add-sale/", add_sale, name="add_sale"),
    path('sales-trends/', sales_trends_chart, name='sales_trends'),
    path('sales-report/', sales_report, name='sales_report'),
    path('sales-reports/', sales_reports, name='sales_reports'),
]

