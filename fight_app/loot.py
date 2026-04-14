from enemy_app.models import loot, loot_gold
import random
from item_app.item_generator import item_generator_all


def loot_generator(player, enemy):

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
                    
    return loot_obtained

    
def loot_created(gold_obtained, loot_obtained, player):
    print(f"Spouštím GENERÁTOR ITEMŮ pro: {player.username} ...")
    for item in loot_obtained:
        item_satus = "inventory"
        item_base_id = str(item["base_id"])
        amount = 1
        item_generator_all(user=player.username, item_status=item_satus, item_base_id=item_base_id, amount=amount)
        
    print(f"Spouštím GENERÁTOR ZLATA pro: {player.username} ...")
    if gold_obtained:
        gold_sum = sum(gold_obtained)
        player.gold += gold_sum
    player.save()


def loot_gold_generator(enemy):
    possible_loot_gold = loot_gold.objects.filter(enemy=enemy)
    
    gold_obtained = []
    
    for i in possible_loot_gold:
        if random.randint(1, 100) <= i.drop_rate:
            gold_obtained.append(random.randint(i.drop_min_amount, i.drop_max_amount))     
    return gold_obtained