# NAČÍTÁNÍ KNIHOVEN
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import random


# NAČÍTÁNÍ MODELU
from profile_app.models import Player_info, Player_Items
from item_app.models import Item_default

# NAČÍTÁNÍ FUNKCÍ
from profile_app.economy import gold_plus
from profile_app.lvl_xp_def import xp_plus
from profile_app.atributs import atr_up, atr_role_default, hp_update, dmg_update
from item_app.item_generator import item_generator_all
from fight_app.fight import fight


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_player_profile(request):
    
    user = request.user
    player = Player_info.objects.filter(username=user).first()
    all_items = Player_Items.objects.all().filter(player=player)  # Získáme všechny položky patřící hráči
    
    print(f"DEBUG: HP hráče {user.username} je {player.hp_max}")  # Debug výpis HP hráče
    
    if not player:
        return Response({"error": "Profil nenalezen"}, status=status.HTTP_404_NOT_FOUND)
    
    dmg_update(player=user)
        
    return Response({
        
        # base info
        "username": user.username,
        "lvl": player.lvl,
        "xp": player.xp,
        "gold": player.gold,
        
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
        
        # items
        "all_items": [{
            "item_status": item.item_status,
            "item_id": item.item_id,
            "item_name": item.name,
            "item_description": item.description,
            "item_category": item.category,
            "item_dmg_type": item.dmg_type,
            "lvl_req": item.lvl_req,
            "item_rarity": item.rarity,
            "price": item.price,
            "dmg_min": item.dmg_min,
            "dmg_max": item.dmg_max,
            "dmg_avg": item.dmg_avg,
            "armor": item.armor,
            "item_bonus": item.item_bonus,
        } for item in all_items],
        
        # EQP
        "weapon_equipped": player.weapon,
        "armor_equipped": player.armor,

        
    }, status=status.HTTP_200_OK)


# SOUBOJE
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def init_fight(request):
    print("Funkce init_fight byla zavolána!")
    
# NAČTENÍ DAT Z FRONTENDU
    user = request.user
    enemy_init_name = request.data.get('enemy_init_name')

    if not enemy_init_name:
        return Response({"error": "Chybí název nepřítele"}, status=status.HTTP_400_BAD_REQUEST)

    if not user:
        return Response({"error": "Profil hráče nenalezen"}, status=status.HTTP_404_NOT_FOUND)
    
    if not enemy_init_name:
        return Response({"error": "Nepřítel nenalezen"}, status=status.HTTP_404_NOT_FOUND)
    
# AKTUALIZACE STATŮ:
    dmg_update(player=user)     
    
# ZAVOLÁNÍ FUNKCE PRO SOUBOJ
    result = fight(player=user, enemy_init_name=enemy_init_name)
    
    
# VRÁCENÍ VÝSLEDKU FRONTENDU
    return Response({"message": f"Výsledek souboje: {result}"}, status=status.HTTP_200_OK)




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
    
    # 1. Kontrola platnosti dat a sečtení všech požadovaných bodů
    for atr_name, amount in updates.items():
        if atr_name not in valid_atrs:
            return Response({"error": f"Neplatný název statu: {atr_name}"}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(amount, int) or amount < 0:
            return Response({"error": "Neplatná hodnota pro zvýšení"}, status=status.HTTP_400_BAD_REQUEST)
        
        total_requested_points += amount
        
    # 2. Kontrola, zda má hráč dostatek bodů na celou dávku
    if player.atr_points < total_requested_points:
        return Response({"error": "Nedostatek atributových bodů na tuto operaci"}, status=status.HTTP_400_BAD_REQUEST)

    
    atr_up(user=user, updates=updates)
    
    # Volitelné: Načtení aktuálních dat pro přesnou zprávu
    player.refresh_from_db()
    
    # aktualizace DMG po změně atributů
    dmg_update(player=user)
    
    return Response({"message": f"Úspěšně rozděleno {total_requested_points} bodů."}, status=status.HTTP_200_OK)



# ADMIN - PŘIDÁVÁNÍ GOLDŮ
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_plus_gold(request):
    print("Funkce admin_plus_gold byla zavolána!")
    user = request.user # Django User objekt
    amount = request.data.get('amount') 

    try:
        amount = int(amount)
    except (TypeError, ValueError):
        return Response({"error": "Parametr 'amount' musí být celé číslo"}, status=status.HTTP_400_BAD_REQUEST)

    if amount <= 0:
        return Response({"error": "Parametr 'amount' musí být kladné číslo"}, status=status.HTTP_400_BAD_REQUEST)

    # Funkce gold_plus z economy.py si už sama hráče v databázi vyhledá.
    # Stačí jí předat 'user' a vyhodnotit, jestli vrátila True nebo False.
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
    
    item_status = "inventory"
    
    item_generator_all(user=user, item_status=item_status, item_base_id=random_item.item_base_id)
    
    # aktualizace DMG po přidání nové zbraně do inventáře
    dmg_update(player=user)

    return Response({"message": f"Náhodná věc úspěšně vygenerována pro hráče {user.username}"}, status=status.HTTP_200_OK)


# NASAZOVÁNÍ A SUNDÁVÁNÍ VĚCÍ (OPTIMISTICKÝ UPDATE)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_equip(request):
    user = request.user

    item_name = request.data.get('item_name')
    new_status = request.data.get('new_status')
    item_id = request.data.get('item_id')

    if new_status not in ['equipped', 'inventory']:
        return Response({"error": "Neplatný status položky"}, status=status.HTTP_400_BAD_REQUEST)
        

    player = Player_info.objects.filter(username=user).first()
    if not player:
        return Response({"error": "Profil hráče nebyl nalezen"}, status=status.HTTP_404_NOT_FOUND)
    
    item = Player_Items.objects.filter(item_id=item_id).first()
    
    if not item:
        return Response({"error": "Položka nebyla nalezena"}, status=status.HTTP_404_NOT_FOUND)
    
    
# USPĚŠNÉ NASAZENÍ / SUNDÁNÍ
    else:
        if new_status == 'equipped':
            if item.category == 'weapon' and player.weapon:
                return Response({"error": "Již máte vybavenou zbraň"}, status=status.HTTP_400_BAD_REQUEST)
            if item.category == 'armor' and player.armor:
                return Response({"error": "Již máte vybavenou zbroj"}, status=status.HTTP_400_BAD_REQUEST)
            if item.category == 'weapon':
                player.weapon = True
            if item.category == 'armor':
                player.armor = True
        elif new_status == 'inventory':
            if item.category == 'weapon':
                player.weapon = False
            if item.category == 'armor':
                player.armor = False
            
        item.item_status = new_status
        item.save()
        
    # aktualizace DMG po změně vybavení
        dmg_update(player=user)
        player.save()
        

    
        return Response({"message": f"Status položky '{item_name}' úspěšně změněn na '{new_status}'"}, status=status.HTTP_200_OK)
    
    

# REGISTRACE UŽIVATELE
@api_view(['POST'])
@permission_classes([AllowAny]) # Registrace musí být přístupná všem
def registrace(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    gender = request.data.get('gender')
    role = request.data.get('role') 
 
 
# convertování hodnot z frontendu na hodnoty pro databázi
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
    hp_update(player=player, update_type='registrace')

    player.save()

    # Přiřazení základních atributů podle role
    atr_role_default(user=user, role=role)
    
    # přiřazení základní výbavy
    items_id = [1,2]
    for i in items_id:
        item_generator_all(user=user, item_status="inventory", item_base_id=i)
    
    # přiřazení základních atributů podle role a aktualizace HP
    dmg_update(player=user)
    
    return Response({"message": f"Registrace proběhla úspěšně: Jméno: {username}, Role: {role}, Pohlaví: {gender}"}, status=status.HTTP_201_CREATED)

    
    
    # Vytvoření tokenu pro okamžité přihlášení po registraci
    token = Token.objects.create(user=user)
    
    return Response({"token": token.key, "message": "Registrace proběhla úspěšně"}, status=status.HTTP_201_CREATED)
    
    
# LOGIN UŽIVATELE - VLASTNÍ IMPLEMENTACE (NEPOUŽÍVÁME DJANGO REST FRAMEWORK TOKEN AUTH)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Autentizace uživatele
    user = authenticate(username=username, password=password)

    if user:
        # Pokud uživatel existuje a heslo sedí, získáme nebo vytvoříme token
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "username": user.username,
            "message": "Přihlášení úspěšné"
        }, status=status.HTTP_200_OK)
    
    return Response({"error": "Neplatné přihlašovací údaje"}, status=status.HTTP_400_BAD_REQUEST)



