from django.urls import path
from . import views
from django.urls import path
from .views import add_category,add_product
from .views import add__product
from .views import product_stock_graph
from .views import  generate_product_pdf
from .views import add_supplier
from .views import save_supplier
from django.urls import path
from .views import generate_pdf


urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path("add-category/", add_category, name="add_category"),
    path("add_product/", add_product, name="add_product"),
    path('get_categories/', add_product, name='get_categories'),
    path('get-categories/', views.get_categories, name='get-categories'),  # AJAX endpoint
    path('add__product/', add__product, name='add__product'),
    path("product-stock-graph/", product_stock_graph, name="product_stock_graph"),
    path('generate_product_pdf/', generate_product_pdf, name='generate_product_pdf'),
    path('supplier_list/', add_supplier, name='supplier_list'),
    path("save_supplier/", save_supplier, name="save_supplier"),
    path('view_cargo/', views.view_cargo, name='view_cargo'),
    path('add_cargo/', views.add_cargo, name='add_cargo'),
    path('update_cargo/<int:cargo_id>/', views.update_cargo, name='update_cargo'),
    path('delete_cargo/<int:cargo_id>/', views.delete_cargo, name='delete_cargo'),
    path('generate_pdf_report/', views.generate_pdf_report, name='generate_pdf_report'),
    path("download-stock-report/", generate_pdf, name="download_stock_report"),
  
]
