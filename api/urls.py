from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_spojeni, name='test_spojeni'), #
    path('registrace/', views.registrace, name='registrace'),
    path('login/', views.login_view, name='login'), #custome přihlášneí
]