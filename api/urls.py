from django.urls import path
from . import views

urlpatterns = [
    path('registrace/', views.registrace, name='registrace'),
    path('login_view/', views.login_view, name='login_view'), #custome přihlášneí
    path('admin_plus_gold/', views.admin_plus_gold, name='admin_plus_gold'),
    path('admin_plus_xp/', views.admin_plus_xp, name='admin_plus_xp'),
    path('profile/', views.get_profile, name='player_profile'),
    path('add_atr/', views.add_atr, name='add_atr'),
    path('admin_random_item/', views.admin_random_item, name='admin_random_item'),
    path('toggle_equip/', views.toggle_equip, name='toggle_equip'),
    path('init_fight/', views.init_fight, name='init_fight'),
    path('sell_item/', views.sell_item, name='sell_item'),
    path('dungeon/<int:dungeon_id>/', views.get_dungeon_details, name='dungeon_details'),
    path('get_all_upgrades/', views.get_all_upgrades, name='get_all_upgrades'),
]