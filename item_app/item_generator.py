from profile_app.models import Player_info, Player_Items_EQP_ABLE, Player_Item_Material
from .models import Item_default, All_Items_Bonus
import random
from item_app.stack_manage import stacks_items


# ZÁKLADNÍ GENEROVÁNÍ ITEMŮ (SPECVIFICKÉ VĚCI SE GENERUJÍ V SEPARÁTNÍ FUNKCI, ABY TO BYLO PŘEHLEDNĚJŠÍ)

def item_generator_all(user, item_status, item_base_id, amount):

    player = Player_info.objects.get(username=user)

    item_category = Item_default.objects.get(item_base_id=item_base_id).category
    
# NAČTENÍ KONKRÉTNÍHO ITEMU I S JEHO SPECIFIÝMI INFORMACEMI
    
    if item_category == "weapon":
        item = Item_default.objects.select_related('weapon_details').get(item_base_id=item_base_id)
        dmg_type = item.weapon_details.dmg_type
        
    elif item_category == "armor":
        item = Item_default.objects.select_related('armor_details').get(item_base_id=item_base_id)
        dmg_type = item.armor_details.dmg_type
        
    elif item_category == "helmet":
        item = Item_default.objects.select_related('helmet_details').get(item_base_id=item_base_id)
        dmg_type = item.helmet_details.dmg_type

    elif item_category == "boots":
        item = Item_default.objects.select_related('boots_details').get(item_base_id=item_base_id)
        dmg_type = item.boots_details.dmg_type

    elif item_category == "amulet":
        item = Item_default.objects.select_related('amulet_details').get(item_base_id=item_base_id)
        dmg_type = None

    elif item_category == "ring":
        item = Item_default.objects.select_related('ring_details').get(item_base_id=item_base_id)
        dmg_type = None

    elif item_category == "talisman":
        item = Item_default.objects.select_related('talisman_details').get(item_base_id=item_base_id)
        dmg_type = None

    elif item_category == "pet":
        item = Item_default.objects.select_related('pet_details').get(item_base_id=item_base_id)
        dmg_type = None

    elif item_category == "material":
        item = Item_default.objects.select_related('material_details').get(item_base_id=item_base_id)
        dmg_type = None

    elif item_category == "useable":
        item = Item_default.objects.select_related('useable_details').get(item_base_id=item_base_id)
        dmg_type = None

    else:
        item = Item_default.objects.get(item_base_id=item_base_id)
        dmg_type = None


# SPECIÁLNĚ PRO ZBRANĚ
    if item.category == "weapon":
        dmg_min, dmg_max, dmg_avg = weapon_generator(player.lvl, item.weapon_details.dmg_base)
        base_attack_speed = item.weapon_details.plus_attack_speed
        random_factor_attack_speed = random.uniform(0.8, 1.2) # náhodný faktor pro rychlost útoku (±20%)
        attack_speed_weapon = round(base_attack_speed * random_factor_attack_speed, 2)
        
    else:
        dmg_min = None
        dmg_max = None
        dmg_avg = None
        attack_speed_weapon = None
    
# HODNOTA BRNĚNÍ

    if item.category == "armor" or item.category == "helmet" or item.category == "boots":
        armor = armor_generator(player.lvl, item.item_base_id)
    else:
        armor = None

# SPECIÁLNĚ PRO BRNĚNÍ:

    if item.category == "armor":
        attack_speed_armor = random.uniform(item.armor_details.min_minus_attack_speed, item.armor_details.max_minus_attack_speed) if item.armor_details.max_minus_attack_speed else None
        armor_hp_bonus = item.armor_details.plus_hp if item.armor_details.plus_hp else 0
    else:
        attack_speed_armor = None
        armor_hp_bonus = 0

    print(f"TEST: attack_speed_armor: {attack_speed_armor}")

# SPECIÁLNĚ PRO HELMY
    if item.category == "helmet":
        attack_speed_helmet = random.uniform(item.helmet_details.min_minus_attack_speed, item.helmet_details.max_minus_attack_speed)
    else:
        attack_speed_helmet = None
        
# PECIÁLNĚ PRO BOTY
    if item.category == "boots":
        base_attack_speed_boots = item.boots_details.plus_percent_attack_speed
        random_factor_attack_speed_boots = random.uniform(0.9, 1.1) # náhodný faktor pro rychlost útoku (±10%)
        attack_speed_boots = round(base_attack_speed_boots * random_factor_attack_speed_boots, 2)
    else:
        attack_speed_boots = None

# SPECIÁLNĚ PRO AMULETY
    if item.category == "amulet":
        all_atr_bonus_amulet = item.amulet_details.all_atr_bonus if item.amulet_details.all_atr_bonus else 0
    else:
        all_atr_bonus_amulet = None
        
# SPECIÁLNĚ PRO PRSTENY
    if item.category == "ring":
        all_atr_bonus_ring = item.ring_details.all_atr_bonus if item.ring_details.all_atr_bonus else 0
    else:
        all_atr_bonus_ring = None


# SPECIÁLNĚ PRO TALISMANY
    if item.category == "talisman":
        talisman_bonus_name, talisman_bonus_value, talisman_bonus_type = talisman_generator()

# SPECIÁLNĚ PRO PETY
    if item.category == "pet":
        
        pet_lvl = 1 # <-- ZATÍM BUDE VŽDYCKY LVL 1 PŘI DROPU
        
        pet_armor_bonus = random.uniform(item.pet_details.min_armor_bonus, item.pet_details.max_armor_bonus) if item.pet_details.max_armor_bonus else None
        
        pet_dmg_bonus = random.uniform(item.pet_details.min_dmg_bonus, item.pet_details.max_dmg_bonus) if item.pet_details.max_dmg_bonus else None
        
        pet_hp_bonus = random.uniform(item.pet_details.min_hp_bonus, item.pet_details.max_hp_bonus) if item.pet_details.max_hp_bonus else None
        
        pet_prum_skoda_bonus = random.uniform(item.pet_details.min_prum_skoda_bonus, item.pet_details.max_prum_skoda_bonus) if item.pet_details.max_prum_skoda_bonus else None


# RARITA

    if item.specific_rarity:
        gen_rarity = item.specific_rarity
    else:
        items_with_rarity = ['weapon', 'armor', 'helmet', 'boots', 'amulet', 'ring', 'talisman']
        if item.category in items_with_rarity:
            gen_rarity = rarity_generator(player.lvl)

        else:
            gen_rarity = "common"

# CENA
    price_ks, price_all = price_generator(item, gen_rarity, player.lvl, amount)
    
# BONUSY   
    # jelikož tady se to ukládá do slovníku tak to nechci komplikovat dalšíé funkcí
    
    item_with_bonus = ['weapon','armor', 'helmet', 'boots', 'amulet', 'ring', 'talisman']
    
    if item.category in item_with_bonus:

        # GENEROVÁNÍ BONUSŮ ITEMU
        all_bonuses = list(All_Items_Bonus.objects.all())

        if gen_rarity == "common":
            bonus_slots = 0
        elif gen_rarity == "rare":
            bonus_slots = 1
        elif gen_rarity == "epic":
            bonus_slots = 2
        elif gen_rarity == "legendary":
            bonus_slots = 3
        else:
            bonus_slots = 0

        bonusy = {}

        # Ujistíme se, že máme co generovat a že máme v databázi dostatek unikátních bonusů
        if bonus_slots > 0 and len(all_bonuses) >= bonus_slots:
            
            # Vybere X unikátních bonusů (nikdy nevybere dva stejné!)
            vybrane_bonusy = random.sample(all_bonuses, bonus_slots)
            
            # Projdeme vybrané bonusy a každému přiřadíme hodnotu
            for bonus in vybrane_bonusy:
                
                bonus_value = round(random.uniform(bonus.min_value, bonus.max_value), 1)
                
                bonusy[bonus.bonus_type] = bonus_value 
        else:
            bonusy = {}
        
    else:
        bonusy = {}


# VYTVOŘENÍ PŘEDMĚTU PRO HRÁČE
    if item.category in ['weapon', 'armor', 'helmet', 'boots', 'amulet', 'ring', 'talisman', 'pet']:
        Player_Items_EQP_ABLE.objects.create(
        
        # OBECNÉ
            player=player,
            item_base_id=item_base_id,
            name = item.name,
            description=item.description,
            item_img_ozn=item.item_img_ozn,
            item_status=item_status,
            stack_able=False,
            
            amount=amount,
            category=item.category,
            lvl_req=item.lvl_req,
            shop_max_lvl_drop=item.shop_max_lvl_drop,
            
            rarity=gen_rarity,
            item_bonusy=bonusy,
            price_ks=price_ks,
            price_all=price_all,


            armor=armor if item.category in ["armor", "helmet", "boots"] else None, # BRNĚNÍ, HELMY, BOTY  
            dmg_type=dmg_type if item.category in ["armor", "helmet", "boots"] else None,
        
        # ATTACK SPEED - U ZBRANÍ, BRNĚNÍ, HELMŮ A BOT
            attack_speed_weapon=attack_speed_weapon if item.category == "weapon" else None,
            attack_speed_armor=attack_speed_armor if item.category == "armor" else None,
            attack_speed_helmet=attack_speed_helmet if item.category == "helmet" else None,
            attack_speed_boots=attack_speed_boots if item.category == "boots" else None,
        
    
        # POUZE ZBRANĚ
            dmg_min=dmg_min if item.category == "weapon" else None,
            dmg_max=dmg_max if item.category == "weapon" else None,
            dmg_avg=dmg_avg if item.category == "weapon" else None,
            
        # POUZE BRNĚNÍ
            plus_hp=armor_hp_bonus if item.category == "armor" else None,

        # POUZE AMULETY
            all_atr_bonus_amulet=all_atr_bonus_amulet if item.category == "amulet" else None,
            
        # POUZE PRSTENY
            all_atr_bonus_ring=all_atr_bonus_ring if item.category == "ring" else None,
        
        # POUZE TALISMAN
            talisman_bonus_name=talisman_bonus_name if item.category == "talisman" else None,
            talisman_bonus_type = talisman_bonus_type if item.category == "talisman" else None,
            talisman_bonus_value=talisman_bonus_value if item.category == "talisman" else None,
            
        # POUZE PRO PETY
            pet_lvl=pet_lvl if item.category == "pet" else None,
            pet_armor_bonus=pet_armor_bonus if item.category == "pet" else None,
            pet_dmg_bonus=pet_dmg_bonus if item.category == "pet" else None,
            pet_hp_bonus=pet_hp_bonus if item.category == "pet" else None,
            pet_prum_skoda_bonus=pet_prum_skoda_bonus if item.category == "pet" else None,
        
        )
        
    elif item.category == "material":
        # Pokud hráč již má tento materiál, aktualizujeme množství, jinak vytvoříme nový záznam
        if Player_Item_Material.objects.filter(player=player, item_base_id=item_base_id, rarity=gen_rarity).exists():

            existing_item = Player_Item_Material.objects.get(player=player, item_base_id=item_base_id, rarity=gen_rarity)
            existing_item.amount += amount
            existing_item.save()
            
        else:
            Player_Item_Material.objects.create(
                player=player,
                item_base_id=item_base_id,
                name=item.name,
                description=item.description,
                item_img_ozn=item.item_img_ozn,
                category=item.category,
                
                item_status=item_status,
                amount=amount,
                
                lvl_req=item.lvl_req,
                rarity=gen_rarity,
                price_ks=price_ks,
                price_all=price_all,
                stack_able=True,
            )
            stacks_items(player)
        return True
    
    
    
    
# PODPŮRNÉ FUNKCE    
def armor_generator(player_lvl, item_base_id):

    item = Item_default.objects.get(item_base_id=item_base_id)
    
    if item.category == "armor":
        item_armor_base = item.armor_details.armor_base
    elif item.category == "helmet":
        item_armor_base = item.helmet_details.armor_base
    elif item.category == "boots":
        item_armor_base = item.boots_details.armor_base
    else:
        item_armor_base = 0
        
    
    
    lvl_multiplier = player_lvl/10 # lvl 15 = 1.5
    
    random_factor_avg = random.uniform(0.8, 1.2) # náhodný faktro pro generování obrany (±20%)
    
    armor = round((item_armor_base * (1 + lvl_multiplier))* random_factor_avg)
    
    return armor

def weapon_generator(player_lvl, item_dmg_base):


    lvl_multiplier = player_lvl/10 # lvl 15 = 1.5
    
    random_factor_avg = random.uniform(0.9, 1.1) # náhodný faktor pro průměrné poškození (±10%)
    random_factor_min = random.uniform(0.7, 0.9) # náhodný faktor pro minimální poškození (70% - 90% z průměrného)
    random_factor_max = random.uniform(1.1, 1.3) # náhodný faktor pro maximální poškození (110% - 130% z průměrného)
    
    
    dmg_avg = round((item_dmg_base * (1 + lvl_multiplier))* random_factor_avg)
    dmg_min = round(dmg_avg * random_factor_min)
    dmg_max = round(dmg_avg * random_factor_max)
    
    return dmg_min, dmg_max, dmg_avg

def rarity_generator(player_lvl):
    
    rarity_koef = player_lvl * 2
    rarity_roll = random.randint(1,rarity_koef)
    
    if rarity_roll >= 80: # od lvlu 40
        gen_rarity = "legendary"
    elif rarity_roll >= 50: # od lvlu 25
        gen_rarity = "epic"
    elif rarity_roll >= 20: # od lvlu 10
        gen_rarity = "rare"
    else: 
        gen_rarity = "common" # od lvlu 1
        
    return gen_rarity


def price_generator(item, rarity, player_lvl, amount):
    
    
    base_price = item.lvl_req / 10 # lvl 15 = 1.5, ,lvl 1 = 0.1
    
    rarity_multiplier = {
        'common': 1,
        'rare': 1.5,
        'epic': 2.5,
        'legendary': 5,
    }
    
    category_multiplier = {
        'weapon': 2,
        'armor': 1.5,
        'helmet': 1.2,
        'boots': 1.2,
        'amulet': 1.3,
        'ring': 1.3,
        'talisman': 1.1,
        'pet': 3,
        'material': 0.5,
        'useable': 0.2,
        'other': 0.1,
    }
    
    random_factor = random.uniform(0.8, 1.2) # náhodný faktor pro cenu (±20%)
    
    price_ks = round(((base_price * rarity_multiplier[rarity]) * category_multiplier[item.category] * random_factor), 2)
    
    price_all = price_ks * amount

    
    return price_ks, price_all
    

def talisman_generator():
    all_bonuses = All_Items_Bonus.objects.all()
    
    chose_bonus = random.choice(all_bonuses)
    
    talisman_bonus_name = chose_bonus.name
    
    talisman_bonus_type = chose_bonus.bonus_type
    
    min_value = chose_bonus.min_value
    max_value = chose_bonus.max_value
    talisman_bonus_value = random.uniform(min_value, max_value)
    
    
    
    return talisman_bonus_name, talisman_bonus_value, talisman_bonus_type