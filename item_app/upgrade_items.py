from profile_app.models import Player_Items_EQP_ABLE

def upgrade_item(item_id):
    
# FRONTEND KONTROLUJE, JESTLI MÁ HRÁČ DOSTATEK MATERIÁLŮ, ABY MOHL PROVÉST UPGRADE, TAKŽE TADY UŽ NENÍ POTŘEBA KONTROLOVAT MATERIÁLY

# PETI MAJÍ VLASTNÍ LOGIKU VYLEPŠOVÁNÍ 

    item = Player_Items_EQP_ABLE.objects.get(item_id=item_id)
    
    if item.item_lvl >= 10:
        raise ValueError("ITEM JE UŽ MAXIMÁLNĚ VYLEPŠENÝ")
    
    new_lvl = item.item_lvl + 1
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