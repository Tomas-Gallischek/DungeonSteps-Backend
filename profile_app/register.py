from .models import Player_info
from item_app.item_generator import item_generator_all
from item_app.models import Item_default

def admin_register(user):
    player = Player_info.objects.filter(username=user).first()
    
    player.gold = 999999
    
    player.save()
    
    admin_base_eqp = [1401, 2401, 3101, 4401, 5401, 6401]
    
    for i in admin_base_eqp:
        item_generator_all(user=user, item_status="inventory", item_base_id=i, amount=1)
        
    # MATERIAL (prvních 20 base ID jsou materiály 1. lokace):
    
    admin_base_materials = Item_default.objects.select_related('material_details').filter(category='material')
    
    
    for i in admin_base_materials:
        print(f"GENERUJI ITEM S BASE_ID: {i.item_base_id}")
        item_generator_all(user=user, item_status="inventory", item_base_id=i.item_base_id, amount=1000) # 1000 od každého

    
    

def default_hp_mana(player, update_type):
        
    # POKUD JE ZALOŽENÁ NOVÁ POSTAVA
    if update_type == 'registrace':
        role = player.role
        
        if role == 'Warrior' or role == 'warrior' or role == 'Válečník':
        # HP
            hp_base = 100
            hp_vit_koef = 15
            hp_lvl_koef = 100
        # MANA
            mana_base = 10
            mana_int_koef = 1
            mana_lvl_koef = 10
        elif role == 'Hunter' or role == 'hunter' or role == 'Hraničář':
            hp_base = 80
            hp_vit_koef = 10
            hp_lvl_koef = 80
        # MANA
            mana_base = 20
            mana_int_koef = 2
            mana_lvl_koef = 20
        elif role == 'Mage' or role == 'mage' or role == 'Mág':
            hp_base = 60
            hp_vit_koef = 5
            hp_lvl_koef = 60
        # MANA
            mana_base = 30
            mana_int_koef = 3
            mana_lvl_koef = 30
        else:
            hp_base = 10  # Defaultní zvýšení HP pro neznámé role
            hp_vit_koef = 1
            hp_lvl_koef = 10
            mana_base = 10  # Defaultní zvýšení many pro neznámé role
            mana_int_koef = 1
            mana_lvl_koef = 10

        
        player.hp_base = hp_base
        player.hp_vit_koef = hp_vit_koef
        player.hp_lvl_koef = hp_lvl_koef
        player.mana_base = mana_base
        player.mana_int_koef = mana_int_koef
        player.mana_lvl_koef = mana_lvl_koef
        player.save()

        
def default_atr(user, role):
    player = Player_info.objects.filter(username=user).first()

    if role == 'warrior':
        player.str_base = 5
        player.dex_base = 2
        player.int_base = 1
        player.vit_base = 5
        player.luck_base = 2
        player.prec_base = 2
        player.save()
    elif role == 'hunter':
        player.str_base = 3
        player.dex_base = 5
        player.int_base = 2
        player.vit_base = 3
        player.luck_base = 4
        player.prec_base = 2
        player.save()
    elif role == 'mage':
        player.str_base = 1
        player.dex_base = 3
        player.int_base = 5
        player.vit_base = 2
        player.luck_base = 4
        player.prec_base = 2
        player.save()
