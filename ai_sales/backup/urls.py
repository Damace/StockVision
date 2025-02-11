# backup/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('backup-data/', views.backup_data, name='backup_data'),
]
