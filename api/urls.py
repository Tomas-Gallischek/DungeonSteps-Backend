from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test_spojeni, name='test_spojeni'), #
    path('registrace/', views.registrace, name='registrace'),
    path('login/', views.CustomAuthToken.as_view(), name='api_token_auth'), #custome přihlášneí
]