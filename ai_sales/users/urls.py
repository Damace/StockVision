from django.contrib import admin
from django.urls import path
from django.urls import include
from users.views import index
from .views import user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('customers/', include('customers.urls')),
    path('home/', home_view, name='home'), 
]


