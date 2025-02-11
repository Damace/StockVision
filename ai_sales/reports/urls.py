# In your Django urls.py
from django.urls import path
from . import views
from .views import update_company_profile

urlpatterns = [
    
    path('company_profile/', views.company_profile, name='company_profile'),
    path('save-company-profile/', views.save_company_profile, name='save_company_profile'),
    path('update-company-profile/', update_company_profile, name='update_company_profile'),
    
]





