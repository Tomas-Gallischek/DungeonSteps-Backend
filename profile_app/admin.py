from django.contrib import admin
from .models import Player_info, Player_Items_EQP_ABLE, Player_Item_Material

admin.site.register(Player_info)
admin.site.register(Player_Items_EQP_ABLE)
admin.site.register(Player_Item_Material)



admin.site.site_header = "Player Profile Admin"
admin.site.site_title = "Player Profile Admin Portal"
admin.site.index_title = "Welcome to the Player Profile Admin Portal"




# Register your models here.
