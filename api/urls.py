from django.urls import path
from . import views

urlpatterns = [
    path('registrace/', views.registrace, name='registrace'),
    path('login/', views.login_view, name='login'), #custome přihlášneí
    path('admin_plus_gold/', views.admin_plus_gold, name='admin_plus_gold'),
    path('admin_plus_xp/', views.admin_plus_xp, name='admin_plus_xp'),
]