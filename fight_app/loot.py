from enemy_app.models import loot
import random
from item_app.item_generator import item_generator_all


def loot_generator(player, enemy):
    print(f"Generuji loot pro nepřítele: {enemy.name} (ID: {enemy.id_unique})")
    # 1. Získáme loot tabulku pro nepřítele (předpokládám model 'Loot')
    # select_related('item') načte Item_default, 
    # prefetch_related načte submodely (weapon_details atd.) v jednom dotazu
    possible_loot = loot.objects.filter(enemy=enemy).select_related('item').prefetch_related(
        'item__weapon_details', 
        'item__armor_details', 
        'item__material_details'
    )
    
    loot_obtained = []
    
    for loot_entry in possible_loot:
        base_item = loot_entry.item  # Instance Item_default
        
        for i in range(loot_entry.drop_max_amount):
            if random.randint(1, 100) <= loot_entry.drop_rate:
                
                # Základní data, která mají všechny itemy společná
                item_data = {
                    "name": base_item.name,
                    "base_id": base_item.item_base_id,
                    "category": base_item.category,
                    "stackable": base_item.stack_able,
                    "amount": 1,
                }

                # 2. Dynamické přidání specifických dat podle kategorie
                if base_item.category == 'weapon' and hasattr(base_item, 'weapon_details'):
                    item_data["dmg_base"] = base_item.weapon_details.dmg_base
                    item_data["dmg_type"] = base_item.weapon_details.dmg_type
                
                elif base_item.category == 'armor' and hasattr(base_item, 'armor_details'):
                    item_data["armor_base"] = base_item.armor_details.armor_base
                
                elif base_item.category == 'material' and hasattr(base_item, 'material_details'):
                    item_data["rarity"] = base_item.material_details.rarity
                    item_data["price_ks"] = base_item.material_details.price_ks

                loot_obtained.append(item_data)
                print(f"Získaný loot: {item_data}")
                    
    return loot_obtained

    
def loot_created(loot_obtained, player):
    for item in loot_obtained:
        item_satus = "inventory"
        item_base_id = str(item["base_id"])
        item_category = item["category"]
        amount = 1
        item_generator_all(user=player.username, item_status=item_satus, item_base_id=item_base_id, item_category=item_category, amount=amount)
            

    
    return loot_obtained