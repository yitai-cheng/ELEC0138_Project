"""secure URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2.  mAdd a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mysite.views import confirm, verify, register, get_verification_code, check_credentials
from mysite.views import StaffListView, StaffCreateView, StaffUpdateView, StaffDeleteView
from mysite.views import generate_password_view
from mysite.views import signup_successful

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', confirm, name='confirm'),
    path('verify/', verify, name='verify'),
    path('register/', register, name='register'),
    path('staff_list/', StaffListView.as_view(), name='staff_list'),
    path('staff/create/', StaffCreateView.as_view(), name='staff_create'),
    path('staff/update/<int:pk>/', StaffUpdateView.as_view(), name='staff_update'),
    path('staff/delete/<int:pk>/', StaffDeleteView.as_view(), name='staff_delete'),
    path('get_verification_code/', get_verification_code, name='get_verification_code'),
    path('check_credentials/', check_credentials, name='check_credentials'),
    path('generate_password/', generate_password_view, name='generate_password'),
    path('signup_successful/', signup_successful, name='signup_successful'),

]
