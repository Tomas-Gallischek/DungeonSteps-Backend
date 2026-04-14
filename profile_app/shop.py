from .models import Player_info, Player_Items_EQP_ABLE
from item_app.models import Item_default
import random
from item_app.item_generator import item_generator_all

def shop_reset(user):
    player = Player_info.objects.get(username=user)
    items_in_shop = Player_Items_EQP_ABLE.objects.filter(player=player, item_status="shop")
    items_in_shop.delete()
    passible_items = Item_default.objects.select_related('weapon_details', 'armor_details').all()
    passible_items = passible_items.filter(category__in=["weapon", "armor"])
    passible_items = passible_items.filter(lvl_req__lte=player.lvl)
    passible_items = passible_items.filter(shop_max_lvl_drop__gte=player.lvl)
    print(f"Počet itemů, které můžu vygenerovat do obchodu pro {user}: {passible_items.count()}")
    
    for item in range(8): # <-- POČET POLOŽEK V OBCHODĚ
        random_item = random.choice(passible_items)
        item_generator_all(user=user,
                           item_status="shop",
                           item_base_id=random_item.item_base_id,
                           amount=1
                           )
        print(f"Vygeneroval jsem item {random_item.name} do obchodu pro: {user}")
    
    return True
    
    
    
    
    
    
