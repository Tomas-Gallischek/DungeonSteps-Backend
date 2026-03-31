from enemy_app.models import loot
import random
from item_app.item_generator import item_generator_all
from item_app.models import Item_default


def loot_generator(player, enemy):
    passible_loot = loot.objects.filter(enemy=enemy)
    all_items = Item_default.objects.all()

    loot_obtained = []
    
    if passible_loot.exists():
        for item in passible_loot:
            drop_rate = item.drop_rate
            drop_amount = item.drop_max_amount
            item_name = item.item.name
            base_id = all_items.get(name=item_name).item_base_id
            for i in range(drop_amount):
                if random.randint(0, 100) <= drop_rate:
                    loot_obtained.extend([{
                        "item_name": item_name,
                        "base_id": base_id,
                        "item_category": item.item.category,
                    }])
                    
    return loot_obtained

    
def loot_created(loot_obtained, player):
    for item in loot_obtained:
        item_satus = "inventory"
        item_base_id = str(item["base_id"])
        item_category = item["item_category"]
        amount = 1
        item_generator_all(user=player.username, item_status=item_satus, item_base_id=item_base_id, item_category=item_category, amount=amount)
            

    
    return loot_obtained