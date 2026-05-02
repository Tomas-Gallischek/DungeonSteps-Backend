from profile_app.models import Player_Items_EQP_ABLE, Player_info, Player_Item_Material
from profile_app.economy import gold_plus
from item_app.models import ItemUpgrade, Item_default, UpgradeMaterial
import random

def upgrade_item(item_id, base_id):
    # FRONTEND KONTROLUJE, JESTLI MÁ HRÁČ DOSTATEK MATERIÁLŮ...
    
    item = Player_Items_EQP_ABLE.objects.get(item_id=item_id)
    all_player_material = Player_Item_Material.objects.filter(player=item.player)
    default_item = Item_default.objects.get(item_base_id=base_id)
    
    profile = Player_info.objects.get(username=item.player.username)
    
    if item.item_lvl >= 10:
        raise ValueError("ITEM JE UŽ MAXIMÁLNĚ VYLEPŠENÝ")

    target_lvl = item.item_lvl + 1 # Level, na který se vylepšuje
    print(f"BASE:ID: {item.item_base_id}, ITEM:ID: {item.item_id}, AKTUÁLNÍ LVL: {item.item_lvl}, CÍLOVÝ LVL: {target_lvl}")

    # 1. BEZPEČNÉ VYHLEDÁNÍ KONKRÉTNÍHO RECEPTU
    # Zde používáme 'item_id=' pro filtrování přes ForeignKey a přesný cílový level
    upgrade_recipe = ItemUpgrade.objects.filter(
        item=default_item, 
        lvl=target_lvl
    ).first()
    


    # 2. POJISTKA PROTI CHYBÁM
    if not upgrade_recipe:
        raise ValueError(f"Recept pro vylepšení tohoto předmětu na level {target_lvl} neexistuje v databázi!")

    # 3. ZÍSKÁNÍ ŠANCE A VYHODNOCENÍ ÚSPĚCHU
    chance = upgrade_recipe.chance
    print(f"Šance na úspěch z databáze je: {chance} (tedy {chance * 100}%)")

    # Hození pomyslnou kostkou (vygeneruje číslo 0.0 až 1.0)
    roll = random.random()

    
# NEZDAŘENÝ UPGRADE
    if roll > chance:
        print("Upgrade se NEZDAŘIL")
        result = "failure"
        return result
    
# ÚSPĚŠNÝ UPGRADE
    else:
        print("Upgrade se PODAŘIL")
        result = "success"
        new_lvl = item.item_lvl + 1
        
# ODEČTENÍ GOLDŮ:
        goldCost = upgrade_recipe.gold_cost
        print(f"Gold cost pro tento upgrade je: {goldCost}")
        gold_plus(profile.username, -goldCost)
        
# odečítání materiálů:
        this_upgrade = ItemUpgrade.objects.get(item=default_item, lvl=new_lvl)
        materialCost = UpgradeMaterial.objects.filter(upgrade=this_upgrade)
        for material in materialCost:
            material_name = material.material.name
            material_amount = material.amount
            print(f"ODEBÍRÁM: {material_amount} kusů materiálu: {material_name}")
            player_material = all_player_material.get(name=material_name)
            player_material.amount -= material_amount
            player_material.save()
            
        
        if item.category == 'weapon':
            
            dmg_up_koef = 1 + item.weapon_dmg_up_koef
            
            item.dmg_min *= dmg_up_koef
            item.dmg_max *= dmg_up_koef
            item.dmg_avg *= dmg_up_koef
            item.item_lvl = new_lvl
            item.save()
            
        elif item.category == 'armor':
            
            armor_up_koef_ARMOR = 1 + (item.armor_up_koef_ARMOR)
            armor_up_koef_HP = 1 + (item.armor_up_koef_HP)
            
            item.armor *= armor_up_koef_ARMOR
            item.plus_hp *= armor_up_koef_HP
            item.item_lvl = new_lvl
            item.save()
        
        elif item.category == 'helmet':
            
            helmet_up_koef= 1 + item.helmet_armor_up_koef
            
            item.armor *= helmet_up_koef
            item.item_lvl = new_lvl
            item.save()
            
        elif item.category == 'boots':
            
            boots_up_koef_ARMOR = 1 + item.boots_armor_up_koef
            
            boots_up_koef_ATTACK_SPEED = item.boots_attack_speed_up_koef
            
            item.armor *= boots_up_koef_ARMOR
            
            item.attack_speed_boots += boots_up_koef_ATTACK_SPEED 
            
            
            item.item_lvl = new_lvl
            item.save()
            
        elif item.category == 'amulet':
            
            amulet_up_koef = item.amulet_atr_up_koef
            
            item.all_atr_bonus_amulet += amulet_up_koef
            
            
            item.item_lvl = new_lvl
            item.save()
        
        
        elif item.category == 'ring':
            
            ring_up_koef = item.ring_atr_up_koef
            
            item.all_atr_bonus_ring += ring_up_koef

            
            item.item_lvl = new_lvl
            item.save()

        else:
            raise ValueError("NEZNÁMÁ KATEGORIE ITEMU")
        
        
        
        return result