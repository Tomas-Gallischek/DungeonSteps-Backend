# NAČÍTÁNÍ KNIHOVEN
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import random



# NAČÍTÁNÍ MODELU
from profile_app.models import Player_info, Player_Items_EQP_ABLE, Player_Item_Material
from item_app.models import Item_default
from map_app.models import Dungeon, Void, WorldBoss
from enemy_app.models import Enemy
from fight_app.models import fight_log

# NAČÍTÁNÍ FUNKCÍ
from profile_app.economy import gold_plus
from profile_app.lvl_xp_def import xp_plus
from profile_app.register import default_atr, default_hp
from item_app.item_generator import item_generator_all
from profile_app.shop import shop_reset
from fight_app.fight import fight
from fight_app.loot import loot_created

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_shop(request):
    user = request.user
    player = Player_info.objects.filter(username=user).first()
    
    if not player:
        return Response({"error": "Profil hráče nenalezen"}, status=status.HTTP_404_NOT_FOUND)
    
    shop_items = Player_Items_EQP_ABLE.objects.filter(item_status='shop')
    print(f"Načítáno BACKEND {shop_items.count()} položek z obchodu pro hráče {user.username}")
    
    try:
        return Response({
            "items_in_shop": [{
                "item_id": item.item_id,
                "item_img_ozn": item.item_img_ozn,
                "item_base_id": item.item_base_id,
                "item_status": item.item_status,
                "name": item.name,
                "description": item.description,
                "category": item.category,
                "dmg_type": item.dmg_type,
                "lvl_req": item.lvl_req,
                "rarity": item.rarity,
                "price_ks": item.price_ks,
                "price_all": item.price_all,
                "dmg_min": item.dmg_min,
                "dmg_max": item.dmg_max,
                "dmg_avg": item.dmg_avg,
                "armor": item.armor,
                "item_bonus": item.item_bonus,
            } for item in shop_items]
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print(f"Chyba při zpracování dat obchodu: {e}")
        return Response({"error": "Chyba při načítání obchodu"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_player_profile(request):    
    user = request.user
    player = Player_info.objects.filter(username=user).first()
    all_items_eqp_able = Player_Items_EQP_ABLE.objects.all().filter(player=player)  # Získáme všechny vybavitelné položky patřící hráči
    all_items_material = Player_Item_Material.objects.all().filter(player=player)  # Získáme všechny materiály patřící hráči
    
    if not player:
        return Response({"error": "Profil nenalezen"}, status=status.HTTP_404_NOT_FOUND)
    
    player.save()
        
    return Response({
        
        # base info
        "username": user.username,
        "lvl": player.lvl,
        "xp": player.xp,
        "gold": player.gold,
        "role": player.role,
        "avatar_img_ozn": player.avatar_img_ozn,
        
        # atributes
        "str_max": player.str_max,
        "dex_max": player.dex_max,
        "int_max": player.int_max,
        "vit_max": player.vit_max,
        "luck_max": player.luck_max,
        
        # HP
        "hp_base": player.hp_base,
        "hp_stats": player.hp_stats,
        "hp_lvl": player.hp_lvl,
        "hp_eqp": player.hp_eqp,
        "hp_max": player.hp_max,
        "hp_vit_koef": player.hp_vit_koef,
        "hp_lvl_koef": player.hp_lvl_koef,
        
        # points
        "atr_points": player.atr_points,   
        "skill_points": player.skill_points,
        "energy_points": player.energy_points,
        "energy_points_regen_5_minutes": player.energy_points_regen_5_minutes,
        
        # items
        "all_items_eqp_able": [{
            "player": user.username,
            "item_id": item.item_id,
            "item_img_ozn": item.item_img_ozn,
            "item_base_id": item.item_base_id,
            "item_status": item.item_status,
            "amount": item.amount,
            "name": item.name,
            "description": item.description,
            "category": item.category,
            "dmg_type": item.dmg_type,
            "lvl_req": item.lvl_req,
            "rarity": item.rarity,
            "price_ks": item.price_ks,
            "price_all": item.price_all,
            "dmg_min": item.dmg_min,
            "dmg_max": item.dmg_max,
            "dmg_avg": item.dmg_avg,
            "armor": item.armor,
            "item_bonus": item.item_bonus,
        } for item in all_items_eqp_able],
        
        "all_items_material": [{
            "player": user.username,
            "item_id": item.item_id,
            "item_img_ozn": item.item_img_ozn,
            "item_base_id": item.item_base_id,
            "item_status": item.item_status,
            "amount": item.amount,
            "name": item.name,
            "description": item.description,
            "category": item.category,
            "lvl_req": item.lvl_req,
            "rarity": item.rarity,
            "price_ks": item.price_ks,
            "price_all": item.price_all,
        } for item in all_items_material],
        
    }, status=status.HTTP_200_OK)


# MAPA


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dungeon_details(request, dungeon_id):
    try:
        dungeon = Dungeon.objects.get(id=dungeon_id)
    except Dungeon.DoesNotExist:
        return Response({"error": "Dungeon nenalezen."}, status=status.HTTP_404_NOT_FOUND)
    
    player= Player_info.objects.filter(username=request.user).first()
    
    if player.lvl < dungeon.min_level:
        return Response({"error": "Úroveň hráče není dostatečná pro vstup do tohoto dungeonu."}, status=status.HTTP_403_FORBIDDEN)

    enemies_list = list(dungeon.enemies.all().values())

    # 3. Ručně si sestavíme slovník pro dungeon (tvůj zavedený postup)
    dungeon_data = {
        "id": dungeon.id,
        "dungeon_base_id": dungeon.dungeon_base_id,
        "name": dungeon.name,
        "description": dungeon.description,
        "background_img": dungeon.background_img,
        "min_level": dungeon.min_level,
        "enemies": enemies_list  # Zde předáváme ten obrovský seznam se všemi daty o příšerách
    }

    # 4. Odešleme na frontend
    return Response(dungeon_data, status=status.HTTP_200_OK)


# OBCHOD

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def shop_buy(request):
    user = request.user
    player = Player_info.objects.filter(username=user).first()
    
    if not player:
        return Response({"error": "Profil hráče nenalezen"}, status=status.HTTP_404_NOT_FOUND)
    
    item_id = request.data.get('item_id')
    item_name = request.data.get('item_name')
    item_price = request.data.get('item_price')

    if not item_id or not item_name or not item_price:
        return Response({"error": "Chybí informace o položce"}, status=status.HTTP_400_BAD_REQUEST)

    if player.gold < float(item_price):
        return Response({"error": "Nedostatek zlata pro nákup této položky"}, status=status.HTTP_400_BAD_REQUEST)

    gold_plus(user=user, amount=-float(item_price))  # Odečteme cenu zlatem
    Player_Items_EQP_ABLE.objects.filter(item_id=item_id, item_status='shop').update(item_status='inventory', player=player)  # Přesuneme položku z obchodu do inventáře hráče
    
    return Response({"message": f"Úspěšně zakoupeno: {item_name} za {item_price} zlata"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sell_item(request):
    user = request.user
    player = Player_info.objects.filter(username=user).first()
    
    if not player:
        return Response({"error": "Profil hráče nenalezen"}, status=status.HTTP_404_NOT_FOUND)
    
    item_id = request.data.get('item_id')
    item_name = request.data.get('item_name')
    item_price = request.data.get('item_price')
    amount = request.data.get('amount')
    
    
    print(f"PRODÁVÁM {amount} KS POLOŽKY: {item_name} (ID: {item_id}) za cenu {item_price} zlata za kus pro hráče {user.username}")    

    if not item_id or not item_name or not item_price:
        return Response({"error": "Chybí informace o položce"}, status=status.HTTP_400_BAD_REQUEST)

# ZJIŠTĚNÍ JESTLI JE POLOŽKA EQP ABLE NEBO MNATERIAL
    current_item = Player_Items_EQP_ABLE.objects.filter(item_id=item_id, player=player).first() if Player_Items_EQP_ABLE.objects.filter(item_id=item_id, player=player).exists() else None
    current_item = Player_Item_Material.objects.filter(item_id=item_id, player=player).first() if not current_item and Player_Item_Material.objects.filter(item_id=item_id, player=player).exists() else current_item
  
    amount_before = current_item.amount if current_item else 0
  
    if not current_item:
        return Response({"error": "Položka nebyla nalezena v inventáři hráče"}, status=status.HTTP_404_NOT_FOUND)
    
    if current_item:
        gold_plus(user=user, amount=(float(item_price) * float(amount)))
        print(f"Aktuální množství položky {item_name} (ID: {item_id}) v inventáři hráče {user.username} je {amount_before}")
    
        if amount_before == 1:
            current_item.delete()
            print(f"Prodej položky: {item_name} (ID: {item_id}) - všechny položky prodány, položka odstraněna z inventáře hráče {user.username}")
        elif amount >= amount_before:
            current_item.delete()
            print(f"Prodej položky: {item_name} (ID: {item_id}) - všechny položky prodány, položka odstraněna z inventáře hráče {user.username}")
        else:
            current_item.amount -= int(amount)
            current_item.save()
            print(f"Prodej položky: {item_name} (ID: {item_id}) - množství aktualizováno na {current_item.amount} v inventáři hráče {user.username}")
    
        return Response({"message": f"Úspěšně prodáno: {item_name} za {item_price} zlata"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Položka nebyla nalezena v inventáři hráče"}, status=status.HTTP_404_NOT_FOUND) 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def shop_refresh(request):
    
# NAČTENÍ DAT Z FRONTENDU
    user = request.user
    if not user:
        return Response({"error": "Profil hráče nenalezen"}, status=status.HTTP_404_NOT_FOUND)

    gold_plus(user=user, amount=-100)  # Odečteme 100 goldů za refresh obchodu
    shop_reset(user=user)
    
# VRÁCENÍ VÝSLEDKU FRONTENDU
    return Response(status=status.HTTP_200_OK)


# SOUBOJE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def init_fight(request):
    print("FIGHT API OK")
    start = timezone.now()
    print(f"Čas zahájení funkce: {start}")
    
# NAČTENÍ DAT Z FRONTENDU
    user = request.user # HRÁČ
    init_base_id = request.data.get('init_base_id') # ID dungeonu/voidu/world bosse
    fight_type = request.data.get('fight_type') # typ souboje: "dungeon", "void" nebo "world_boss"
    fight_time_minutes = request.data.get('fight_time') # čas souboje v minutách, který posílá frontend
    fight_time_seconds = fight_time_minutes * 60
    
    print(f"Z FRONTENDU: Hráč: {user}, ID souboje: {init_base_id}, Typ souboje: {fight_type}, Čas souboje: {fight_time_minutes} minut")
    
    if not user:
        return Response({"error": "Profil hráče nenalezen"}, status=status.HTTP_404_NOT_FOUND)
    if not init_base_id or not fight_type:
        return Response({"error": "Chybí informace o souboji"}, status=status.HTTP_400_BAD_REQUEST)
    if fight_type not in ["dungeon", "void", "world_boss"]:
        return Response({"error": "Neplatný typ souboje"}, status=status.HTTP_400_BAD_REQUEST)
    if fight_time_minutes is None or not isinstance(fight_time_minutes, (int, float)) or fight_time_minutes <= 0:
        return Response({"error": "Neplatný čas souboje"}, status=status.HTTP_400_BAD_REQUEST)
    
    
# identifikace
    player = Player_info.objects.filter(username=user).first()
    
    if fight_type == "dungeon":
        enemy_instance = Dungeon.objects.filter(dungeon_base_id=init_base_id).first() if Dungeon.objects.filter(dungeon_base_id=init_base_id).exists() else None
        enemy_list = enemy_instance.enemies.all() if enemy_instance else []
        print(f"NAČÍTÁM ENEMY PRO DUNGEON: {enemy_list.count()} příšer načteno pro dungeon s ID {init_base_id}")
        
    if fight_type == "void":
        enemy_instance = Void.objects.filter(void_base_id=init_base_id).first() if Void.objects.filter(void_base_id=init_base_id).exists() else None
        enemy_list = enemy_instance.enemies.all() if enemy_instance else []
        void = enemy_instance
        print(f"NAČÍTÁM ENEMY PRO VOID: {void} {enemy_list.count()} příšer načteno pro void s ID {init_base_id}")
        
    if fight_type == "world_boss":
        enemy_instance = WorldBoss.objects.filter(world_boss_base_id=init_base_id).first() if WorldBoss.objects.filter(world_boss_base_id=init_base_id).exists() else None
        enemy_list = [enemy_instance] if enemy_instance else [] # BOSS JE JEN JEDEN
        print(f"NAČÍTÁM ENEMY PRO WORLD BOSS: {enemy_list.count()} příšer načteno pro world bosse s ID {init_base_id}")

# ODEČTENÍ ENERGIE PŘED SOUBOJEM + AKTUALIZACE DAT:
    player.energy_points -= fight_time_minutes * 1  # Odečteme energii podle času souboje
    player.save()
    
# ZJIŠTĚNÍ STATŮ KONKRÉTNÍCH MOBEK
    passible_enemies_id = []
    for one_enemy in enemy_list:
        passible_enemies_id.append(one_enemy.id_unique)
    
    all_passible_enemies_stats = Enemy.objects.filter(id_unique__in=passible_enemies_id)
    enemy_range_id = all_passible_enemies_stats.values_list('id_unique', flat=True)
    
    fight_duration = 0 # SEKUNDY
    all_turn_logs = []
    enemies_defeded = []
    all_loot_obtained = []
    
    while fight_duration < fight_time_seconds:
        fight_start_time = timezone.now()
        for one_enemy in random.sample(list(enemy_range_id), len(enemy_range_id)):
            enemy = all_passible_enemies_stats.filter(id_unique=one_enemy).first()
            current_time, id_unique, turn_logs, winner, all_loot_obtained = fight(player=player, enemy=enemy)
            
            fight_duration += current_time
            all_turn_logs.extend(turn_logs)
            all_loot_obtained.extend(all_loot_obtained)
            if winner == player.username:
                enemies_defeded.append(id_unique)
            else:
                pass
            
# ČASOVÉ OMEZENÍ SOUBOJE:
            if fight_duration >= fight_time_seconds:
                print("Dosaženo limitu času pro souboje. Ukončuji další souboje.")
                fight_log.objects.create(
                    player=player,
                    all_enemies_defeded=enemies_defeded,
                    defeinitive_winner=player.username,
                    time_start=fight_start_time, 
                    time_end=timezone.now(),
                    time_duration_seconds=fight_duration,
                    turn_logs=all_turn_logs  # JSON pole s asynchronními tahy a relativními časy
                )
                end = timezone.now()
                duration = end - start
                print(f"Čas ukončení funkce: {end}, Celková doba trvání funkce: {duration}")
                
                loot_created(
                    loot_obtained=all_loot_obtained,
                    player=player
                )
                
                return Response({"message": "DOŠEL LIMIT ČASU PRO SOUBOJE"}, status=status.HTTP_200_OK)
                break
            
# HRÁČ PROHRÁL:
            if winner != player.username:
                print("Hráč prohrál souboj. Ukončuji další souboje.")
                fight_log.objects.create(
                    player=player,
                    all_enemies_defeded=enemies_defeded,
                    defeinitive_winner="mobs",
                    time_start=fight_start_time, 
                    time_end=timezone.now(),
                    time_duration_seconds=fight_duration,
                    turn_logs=all_turn_logs  # JSON pole s asynchronními tahy a relativními časy
                )
                
                loot_created(
                    loot_obtained=all_loot_obtained,
                    player=player
                )    

                return Response({"message": "Hráč prohrál souboj. Ukončuji další souboje."}, status=status.HTTP_200_OK)
                break

    

# ZVYŠOVÁNÍ STATŮ
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_atr(request):
    user = request.user
    player = Player_info.objects.filter(username=user).first()
    
    if not player:
        return Response({"error": "Profil nenalezen"}, status=status.HTTP_404_NOT_FOUND)
    
    # Získáme slovník updatů (např. {"str": 2, "vit": 1})
    updates = request.data.get('updates', {})
    
    if not isinstance(updates, dict):
        return Response({"error": "Očekáván slovník s updaty"}, status=status.HTTP_400_BAD_REQUEST)
    
    valid_atrs = ['str', 'dex', 'int', 'vit', 'luck']
    total_requested_points = 0

    for atr_name, amount in updates.items():
        if atr_name not in valid_atrs:
            return Response({"error": f"Neplatný název statu: {atr_name}"}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(amount, int) or amount < 0:
            return Response({"error": "Neplatná hodnota pro zvýšení"}, status=status.HTTP_400_BAD_REQUEST)
        
        total_requested_points += amount
        
    if player.atr_points < total_requested_points:
        return Response({"error": "Nedostatek atributových bodů na tuto operaci"}, status=status.HTTP_400_BAD_REQUEST)

    # AKTUALIZACE STATŮ V DATABÁZI - NA KONCI SE VOLÁ player.save() !!!!
    player.atr_up(updates=updates)
    
    return Response({"message": f"Úspěšně rozděleno {total_requested_points} bodů."}, status=status.HTTP_200_OK)


# NASAZOVÁNÍ A SUNDÁVÁNÍ VĚCÍ (OPTIMISTICKÝ UPDATE)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_equip(request):
    user = request.user
    item_name = request.data.get('item_name')
    new_status = request.data.get('new_status')
    player = Player_info.objects.filter(username=user).first()
    item_id = request.data.get('item_id')
    item = Player_Items_EQP_ABLE.objects.filter(item_id=item_id).first()

    if new_status not in ['equipped', 'inventory']:
        return Response({"error": "Neplatný status položky"}, status=status.HTTP_400_BAD_REQUEST)
        
    if not player:
        return Response({"error": "Profil hráče nebyl nalezen"}, status=status.HTTP_404_NOT_FOUND)
    
    if not item:
        return Response({"error": "Položka nebyla nalezena"}, status=status.HTTP_404_NOT_FOUND)
    
    all_eqp_categories = Player_Items_EQP_ABLE.objects.filter(player=player, item_status='equipped').values_list('category', flat=True)
    
    if new_status == 'inventory':
        item.item_status = 'inventory'
        item.save()
    elif new_status == 'equipped':
        if item.category in all_eqp_categories:
            Player_Items_EQP_ABLE.objects.filter(player=player, category=item.category, item_status='equipped').update(item_status='inventory')
            item.save()
        item.item_status = 'equipped'
        item.save()     
    
    player.save()  # Aktualizace hráče po změně vybavení

    return Response({"message": f"Status položky '{item_name}' úspěšně změněn na '{new_status}'"}, status=status.HTTP_200_OK)
    
    
#--- LOGIN + REGISTRACE ---

@api_view(['POST'])
@permission_classes([AllowAny])
def registrace(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    gender = request.data.get('gender')
    role = request.data.get('role') 

    if gender == 'Muž':
        gender = 'male'
    elif gender == 'Žena':
        gender = 'female'
    else:
        gender = 'other'
        
    if role == 'Válečník':
        role = 'warrior'
    elif role == 'Mág':
        role = 'mage'
    elif role == 'Hraničář':
        role = 'hunter'

    
    
    if not username or not password:
        return Response({"error": "Chybí jméno nebo heslo"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Uživatel již existuje"}, status=status.HTTP_400_BAD_REQUEST)

    # Vytvoření uživatele (Django automaticky hash hesla)
    user = User.objects.create_user(username=username, password=password, email=email)
    
    # Vytvoření profilu hráče
    Player_info.objects.create(username=user)
    
    # přiřazení pohlaví do profilu
    player = Player_info.objects.filter(username=user).first()
       
    player.gender = gender
    player.role = role

    # nastavení základních životů
    default_hp(player=player, update_type='registrace')

    player.save()

    # Přiřazení základních atributů podle role
    default_atr(user=user, role=role)
    
    # přiřazení základní výbavy
    items_id = [1,2]
    item_category = ["weapon", "armor"]
    for i, category in zip(items_id, item_category):
        item_generator_all(user=user, item_status="inventory", item_base_id=i, item_category=category, amount=1)
    
# Vytvoření tokenu pro nového uživatele
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        "token": token.key, 
        "message": f"Registrace proběhla úspěšně: Jméno: {username}, Role: {role}, Pohlaví: {gender}"
    }, status=status.HTTP_201_CREATED)
    
    
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Autentizace uživatele
    user = authenticate(username=username, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "username": user.username,
            "message": "Přihlášení úspěšné"
        }, status=status.HTTP_200_OK)
    
    return Response({"error": "Neplatné přihlašovací údaje"}, status=status.HTTP_400_BAD_REQUEST)



# --- ADMIN CHEAT SEKCE ----

# ADMIN - PŘIDÁVÁNÍ GOLDŮ
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_plus_gold(request):
    print("Funkce admin_plus_gold byla zavolána!")
    user = request.user
    amount = request.data.get('amount') 

    try:
        amount = int(amount)
    except (TypeError, ValueError):
        return Response({"error": "Parametr 'amount' musí být celé číslo"}, status=status.HTTP_400_BAD_REQUEST)

    if amount <= 0:
        return Response({"error": "Parametr 'amount' musí být kladné číslo"}, status=status.HTTP_400_BAD_REQUEST)

    uspech = gold_plus(user=user, amount=amount) 
    
    if not uspech:
        return Response({"error": "Profil hráče nebyl nalezen"}, status=status.HTTP_404_NOT_FOUND)

    return Response({"message": f"Úspěšně odesláno: {amount} zlata pro hráče {user.username}"}, status=status.HTTP_200_OK)


# ADMIN - PŘIDÁVÁNÍ XP
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_plus_xp(request):
    print("Funkce admin_plus_xp byla zavolána!")
    user = request.user 
    amount = request.data.get('amount') 

    try:
        amount = int(amount)
    except (TypeError, ValueError):
        return Response({"error": "Parametr 'amount' musí být celé číslo"}, status=status.HTTP_400_BAD_REQUEST)

    if amount <= 0:
        return Response({"error": "Parametr 'amount' musí být kladné číslo"}, status=status.HTTP_400_BAD_REQUEST)

    player = Player_info.objects.filter(username=user).first()
    if not player:
        return Response({"error": "Profil hráče nebyl nalezen"}, status=status.HTTP_404_NOT_FOUND)

    xp_plus(user=user, xp_amount=amount)

    return Response({"message": f"Úspěšně odesláno: {amount} XP pro hráče {user.username}"}, status=status.HTTP_200_OK)


# ADMIN - PŘIDÁVÁNÍ NÁHODNÉ VĚCI
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_random_item(request):
    print("Funkce admin_random_item byla zavolána!")
    user = request.user 

    player = Player_info.objects.filter(username=user).first()
    if not player:
        return Response({"error": "Profil hráče nebyl nalezen"}, status=status.HTTP_404_NOT_FOUND)



    all_items = Item_default.objects.all()
    random_item = random.choice(all_items)
    item_category = random_item.category
    amount = 1
    
    item_status = "inventory"
    
    item_generator_all(user=user, item_status=item_status, item_base_id=random_item.item_base_id, item_category=item_category, amount=amount)
    
    # aktualizace DMG po přidání nové zbraně do inventáře


    return Response({"message": f"Náhodná věc úspěšně vygenerována pro hráče {user.username}"}, status=status.HTTP_200_OK)