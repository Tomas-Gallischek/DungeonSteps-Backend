from .models import Player_info, Player_Items


def hp_update(player, update_type):
# POKUD ZVYŠUJEME HP ZA LVL
    if update_type == 'lvl_up':
        hp_koef = player.hp_lvl_koef
        player.hp_lvl += (player.lvl * hp_koef)  # Zvýšení HP o koeficient násobený aktuální úrovní hráče   
        player.save()
        
    # POKUD SE ZVÝŠILA VITALITA
    elif update_type == 'atr_change':
        
        vit = player.vit_max
        hp_vit_koef = player.hp_vit_koef
        
        hp_update = vit * hp_vit_koef  # Každý bod vitality zvyšuje HP o koeficient
        player.hp_stats += hp_update
        player.save()
        
    # POKUD JE ZALOŽENÁ NOVÁ POSTAVA
    elif update_type == 'registrace':
        role = player.role
        
        if role == 'Warrior' or role == 'warrior' or role == 'Válečník':
            hp_base = 100
            hp_vit_koef = 15
            hp_lvl_koef = 100
        elif role == 'Hunter' or role == 'hunter' or role == 'Hraničář':
            hp_base = 80
            hp_vit_koef = 10
            hp_lvl_koef = 80

        elif role == 'Mage' or role == 'mage' or role == 'Mág':
            hp_base = 60
            hp_vit_koef = 5
            hp_lvl_koef = 60
        else:
            hp_base = 10  # Defaultní zvýšení HP pro neznámé role
            hp_vit_koef = 1
            hp_lvl_koef = 10

        
        player.hp_base = hp_base
        player.hp_vit_koef = hp_vit_koef
        player.hp_lvl_koef = hp_lvl_koef
        player.save()

    # POKAŽDNÉ ZMMĚNĚ SE AKTUALIZUJE MAXIMÁLNÍ HODNOTA HP
    hp_base = player.hp_base
    hp_stats = player.hp_stats
    hp_eqp = player.hp_eqp
    hp_lvl = player.hp_lvl
    
    new_hp = hp_base + hp_stats + hp_eqp + hp_lvl
    player.hp_max = new_hp
    player.save()



def atr_up(user, updates):    
    player = Player_info.objects.filter(username=user).first()
    
    if not player:
        return False
        
    user_name = player.username
    total_spent = 0
    
    for atr_name, amount in updates.items():
        if amount <= 0:
            continue
            
        atr_name = atr_name.lower()
        
        if atr_name == 'str':
            for i in range(amount):
                player.str_stats += 1

                
        elif atr_name == 'dex':
            for i in range(amount):
                player.dex_stats += 1

                
        elif atr_name == 'int':
            for i in range(amount):
                player.int_stats += 1

                
                
        elif atr_name == 'luck':
            for i in range(amount):
                player.luck_stats += 1
                crit_update(player=player, update_type='luck_change')

                
        elif atr_name == 'vit':
            for _ in range(amount):
                player.vit_stats += 1
                player.vit_max += 1 # <-- Pracovní hodnota kvůlui aktualizaci HP z vitality, která se bude přičítat k max HP
                hp_update(player=player, update_type='atr_change')

                
        else:
            continue
            
        total_spent += amount
    
    if total_spent > 0:
            player.atr_points -= total_spent
            player.save()

            atr_max_update(user_name)
            player.refresh_from_db()
            
            for changed_atr, amount in updates.items():
                if amount > 0:
                    atr_resist_update(player, changed_atr)
            

            dmg_update(user)
            
    return True


def atr_max_update(player):
    user = Player_info.objects.filter(username=player).first()
    
    if not user:
        return False # Pro jistotu, kdyby se hráč nenašel
    
    all_atr = ['str', 'dex', 'int', 'vit', 'luck']
    
    for atr in all_atr:
        base_value = getattr(user, f"{atr}_base")
        stats_value = getattr(user, f"{atr}_stats")
        eqp_value = getattr(user, f"{atr}_eqp")
        max_value = base_value + stats_value + eqp_value
        setattr(user, f"{atr}_max", max_value)
    user.save()
    
    # Ukončíme funkci až poté, co cyklus proběhne pro všechny atributy
    return True
    
        
        
def atr_role_default(user, role):
    player = Player_info.objects.filter(username=user).first()

    if role == 'warrior':
        player.str_base = 5
        player.dex_base = 2
        player.int_base = 1
        player.vit_base = 5
        player.luck_base = 2
        player.save()
    elif role == 'hunter':
        player.str_base = 3
        player.dex_base = 5
        player.int_base = 2
        player.vit_base = 3
        player.luck_base = 4
        player.save()
    elif role == 'mage':
        player.str_base = 1
        player.dex_base = 3
        player.int_base = 5
        player.vit_base = 2
        player.luck_base = 4
        player.save()
        
    atr_max_update(player=user)
        
        
def dmg_update(user):
    player = Player_info.objects.filter(username=user).first()
    weapon = Player_Items.objects.filter(player=player, category='weapon', item_status='equipped').first()
    
    if not player:
        return False # Pro jistotu, kdyby se hráč nenašel

    if weapon:
        if weapon.dmg_type == 'light':
            dmg_atr_value = player.dex_max
            dmg_atr = 'dex'
        elif weapon.dmg_type == 'heavy':
            dmg_atr_value = player.str_max
            dmg_atr = 'str'
        elif weapon.dmg_type == 'magic':
            dmg_atr_value = player.int_max
            dmg_atr = 'int'
            
    elif not weapon:
        no_weapon_base_dmg = player.lvl
        no_weapon_dmg_min = no_weapon_base_dmg * 0.8
        no_weapon_dmg_max = no_weapon_base_dmg * 1.2
        dmg_atr_value = 1
        dmg_atr = 'none'
    else:
        no_weapon_base_dmg = player.lvl
        no_weapon_dmg_min = no_weapon_base_dmg * 0.8
        no_weapon_dmg_max = no_weapon_base_dmg * 1.2
        dmg_atr_value = 1
        dmg_atr = 'none'

        
    player.dmg_atr = dmg_atr
    player.dmg_atr_value = dmg_atr_value
    
    
    dmg_base = dmg_atr_value + weapon.dmg_avg if weapon else no_weapon_base_dmg  # Základní poškození se počítá z atributu a zbraně, pokud je vybavená, jinak z úrovně
    dmg_min = (dmg_base * weapon.dmg_min) if weapon else no_weapon_dmg_min  # Minimální poškození se počítá z základního poškození a zbraně, pokud je vybavená, jinak z úrovně
    dmg_max = (dmg_base * weapon.dmg_max) if weapon else no_weapon_dmg_max  # Maximální poškození se počítá z základního poškození a zbraně, pokud je vybavená, jinak z úrovně
    dmg_avg = (dmg_min + dmg_max) // 2
    

    random_dmg_list = []
    random_dmg_list.clear()  # Vyčistíme předchozí hodnoty, pokud nějaké jsou
    
    player.dmg_base = int(dmg_base)
    player.dmg_min = int(dmg_min)
    player.dmg_max = int(dmg_max)
    player.dmg_avg = int(dmg_avg)
    
    player.save()
    return True


def crit_update(player, update_type):
    if update_type == 'luck_change':
        player.crit_chance = (player.luck_stats // player.lvl)
        if player.crit_chance > 50:
            player.crit_chance = 50
        player.save()
        
        
def atr_resist_update(player, atr):    
    if atr == 'str':
        resist = round((player.str_max // player.lvl), 2)
        if resist > 50:
            resist = 50
        player.str_resist = resist
        
    elif atr == 'dex':
        resist = round((player.dex_max // player.lvl), 2)
        if resist > 50:
            resist = 50
        player.dex_resist = resist
    elif atr == 'int':
        resist = round((player.int_max // player.lvl), 2)
        if resist > 50:
            resist = 50
        player.int_resist = resist
    player.save()
    
    
def armor_update(user):
    player = Player_info.objects.filter(username=user).first()
    armor = 1
    armor_eqp = Player_Items.objects.filter(player=player, category='armor', item_status='equipped').first() or None
    
    if armor_eqp:
        player.armor = armor_eqp.armor
        player.save()
    else:
        player.armor = armor
        player.save()    
    
    player.refresh_from_db()
    return True
