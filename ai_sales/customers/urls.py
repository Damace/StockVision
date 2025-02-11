from django.urls import path
from .views import customer_dashboard

urlpatterns = [
    path('<int:customer_id>/', customer_dashboard, name='customer_dashboard'),
]
