from django.urls import path
from . import views

urlpatterns = [
    path('registrace/', views.registrace, name='registrace'),
    path('login/', views.login_view, name='login'), #custome přihlášneí
    path('admin_plus_gold/', views.admin_plus_gold, name='admin_plus_gold'),
    path('admin_plus_xp/', views.admin_plus_xp, name='admin_plus_xp'),
    path('profile/', views.get_player_profile, name='player_profile'),
    path('add_atr/', views.add_atr, name='add_atr'),
    path('admin_random_item/', views.admin_random_item, name='admin_random_item'),
    path('toggle_equip/', views.toggle_equip, name='toggle_equip'),
    path('init_fight/', views.init_fight, name='init_fight'),
]