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
from profile_app.atributs import atr_up, atr_role_default
from item_app.item_generator import item_generator_all


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_player_profile(request):
    
    user = request.user
    player = Player_info.objects.filter(username=user).first()
    all_items = Player_Items.objects.all().filter(player=player)  # Získáme všechny položky patřící hráči
    
    if not player:
        return Response({"error": "Profil nenalezen"}, status=status.HTTP_404_NOT_FOUND)
        
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
        } for item in all_items]
  
        
    }, status=status.HTTP_200_OK)




# ZVYŠOVÁNÍ STATŮ
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_atr(request):
    user = request.user
    player = Player_info.objects.filter(username=user).first()
    
    if not player:
        return Response({"error": "Profil nenalezen"}, status=status.HTTP_404_NOT_FOUND)
    
    atr_name = request.data.get('atr')
    
    if atr_name not in ['str', 'dex', 'int', 'vit', 'luck']:
        return Response({"error": "Neplatný název stat"}, status=status.HTTP_400_BAD_REQUEST)
    
    if player.atr_points <= 0:
        return Response({"error": "Nedostatek atributových bodů"}, status=status.HTTP_400_BAD_REQUEST)
  
    # FUNKCE PRO ZVÝŠENÍ ATRIBUTŮ
    atr_up(user=user, atr_name=atr_name)
    

    
    return Response({"message": f"Úspěšně zvýšen {atr_name} na {getattr(player, f'{atr_name}_stats')}"}, status=status.HTTP_200_OK)



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
    else:
        item.item_status = new_status
        item.save()
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
    player.save()

    # Přiřazení základních atributů podle role
    atr_role_default(user=user, role=role)
    
    # přiřazení základní výbavy
    items_id = [1,2]
    for i in items_id:
        item_generator_all(user=user, item_status="inventory", item_base_id=i)
    
    
    
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



