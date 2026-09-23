"""
URL configuration for healthbridge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('find_doctor/', views.find_doctor, name='find_doctor'),
    path('hospitals/', views.hospitals, name='hospitals'),
    path('hospital/<int:hospital_id>/', views.hospital_details, name='hospital_detail'),
    path('appointments/', views.appointments, name='appointments'),
    path('book_appointment/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
]
