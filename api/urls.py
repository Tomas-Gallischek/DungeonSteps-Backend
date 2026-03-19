from django.urls import path
from . import views

urlpatterns = [
    # Kivy se bude ptát na adresu: /api/test/
    path('test/', views.test_spojeni, name='test_spojeni'),
]