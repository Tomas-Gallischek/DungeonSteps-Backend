from profile_app.models import Player_info, Player_Items_EQP_ABLE, Player_Item_Material
from .models import Item_default, All_Items_Bonus
import random
from item_app.stack_manage import stacks_items


# ZÁKLADNÍ GENEROVÁNÍ ITEMŮ (SPECVIFICKÉ VĚCI SE GENERUJÍ V SEPARÁTNÍ FUNKCI, ABY TO BYLO PŘEHLEDNĚJŠÍ)

def item_generator_all(user, item_status, item_base_id, item_category, amount):
    print(f"ITEM GENERATOR: {user}, {item_status}, {item_base_id}, {item_category}")
    
# NAČTENÍ KONKRÉTNÍHO ITEMU I S JEHO SPECIFIÝMI INFORMACEMI
    player = Player_info.objects.get(username=user)
    
    if item_category == "weapon":
        item = Item_default.objects.select_related('weapon_details').get(item_base_id=item_base_id)
        dmg_type = item.weapon_details.dmg_type
    elif item_category == "armor":
        item = Item_default.objects.select_related('armor_details').get(item_base_id=item_base_id)
    elif item_category == "material":
        item = Item_default.objects.select_related('material_details').get(item_base_id=item_base_id)

# SPECIÁLNĚ PRO ZBRANĚ
    if item.category == "weapon":
        dmg_min, dmg_max, dmg_avg = weapon_generator(player.lvl, item.weapon_details.dmg_base)
    else:
        dmg_min = None
        dmg_max = None
        dmg_avg = None

# SPECIÁLNĚ PRO BRNĚNÍ
    if item.category == "armor":
        armor = armor_generator(player.lvl, item.armor_details.armor_base)
    else:
        armor = None

# RARITA
    items_with_rarity = ['weapon', 'armor']
    if item.category in items_with_rarity:
        gen_rarity = rarity_generator(player.lvl)

    else:
        gen_rarity = "common"

# CENA
    price_ks, price_all = price_generator(item, gen_rarity, player.lvl, amount)
    
# BONUSY   
# jelikož tady se to ukládá do slovníku tak to nechci komplikovat dalšíé funkcí
    
    item_with_bonus = ['weapon','armor']
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

        print(f"bonusy: {bonusy}")
        
    else:
        bonusy = {}


# VYTVOŘENÍ PŘEDMĚTU PRO HRÁČE
    if item.category in ['weapon', 'armor']:
        Player_Items_EQP_ABLE.objects.create(
            player=player,
            item_base_id=item_base_id,
            name=item.name,
            item_status=item_status,
            amount=amount,
            description=item.description,
            category=item.category,
            dmg_type=dmg_type if item.category == "weapon" else None,
            lvl_req=item.lvl_req,
            rarity=gen_rarity,
            price_ks=price_ks,
            price_all=price_all,
            dmg_min=dmg_min if item.category == "weapon" else None,
            dmg_max=dmg_max if item.category == "weapon" else None,
            dmg_avg=dmg_avg if item.category == "weapon" else None,
            armor=armor if item.category == "armor" else None,
            item_bonus=bonusy if bonusy else None,
        )
        
    elif item.category == "material":
        # Pokud hráč již má tento materiál, aktualizujeme množství, jinak vytvoříme nový záznam
        if Player_Item_Material.objects.filter(player=player, item_base_id=item_base_id).exists():
            print("Hráč již má tento materiál, aktualizuji množství.")
            existing_item = Player_Item_Material.objects.get(player=player, item_base_id=item_base_id)
            existing_item.amount += amount
            existing_item.save()
        else:
            print("Hráč tento materiál ještě nemá, vytvářím nový záznam.")
            Player_Item_Material.objects.create(
                player=player,
                item_base_id=item_base_id,
                item_status=item_status,
                amount=amount,
                name=item.name,
                description=item.description,
                category=item.category,
                lvl_req=item.lvl_req,
                rarity=gen_rarity,
                price_ks=price_ks,
                price_all=price_all,
                stack_able=item.stack_able,
                max_stack=item.max_stack,
            )
            stacks_items(player)
        return True
    
    
    
    
# PODPŮRNÉ FUNKCE    
def armor_generator(player_lvl, item_armor_base):
    print("spuštění generátoru brnění")
    
    lvl_multiplier = player_lvl/10 # lvl 15 = 1.5
    random_factor_avg = random.uniform(0.9, 1.1) # náhodný faktro pro generování obrany (±10%)
    
    armor = round((item_armor_base * (1 + lvl_multiplier))* random_factor_avg)
    return armor

def weapon_generator(player_lvl, item_dmg_base):
    print("spuštění generátoru zbraní")

    lvl_multiplier = player_lvl/10 # lvl 15 = 1.5
    
    random_factor_avg = random.uniform(0.9, 1.1) # náhodný faktor pro průměrné poškození (±10%)
    random_factor_min = random.uniform(0.7, 0.9) # náhodný faktor pro minimální poškození (70% - 90% z průměrného)
    random_factor_max = random.uniform(1.1, 1.3) # náhodný faktor pro maximální poškození (110% - 130% z průměrného)
    
    
    dmg_avg = round((item_dmg_base * (1 + lvl_multiplier))* random_factor_avg)
    dmg_min = round(dmg_avg * random_factor_min)
    dmg_max = round(dmg_avg * random_factor_max)
    
    return dmg_min, dmg_max, dmg_avg

def rarity_generator(player_lvl):
    print("spuštění generátoru rarity")
    
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
    print("spuštění generátoru ceny")
    
    if item.category == "material":
        return (item.material_details.price_ks), (item.material_details.price_ks * amount)
    else:
        price_ks = 1
        price_all = 1
        base_price = item.lvl_req *5
        
        rarity_multiplier = {
            'common': 1,
            'rare': 1.5,
            'epic': 2.5,
            'legendary': 5,
        }
        
        category_multiplier = {
            'weapon': 1.5,
            'armor': 1.2,
            'other': 1,
        }
        
        price_ks = round((base_price * rarity_multiplier[rarity]) * category_multiplier[item.category])
        price_all = price_ks * amount

        
        return price_ks, price_all