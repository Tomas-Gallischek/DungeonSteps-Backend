# NAČÍTÁNÍ KNIHOVEN
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


# NAČÍTÁNÍ MODELU
from profile_app.models import Player_info

# NAČÍTÁNÍ FUNKCÍ
from profile_app.economy import gold_plus
from profile_app.lvl_xp_def import xp_plus
from profile_app.atributs import atr_up, atr_role_default


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_player_profile(request):
    user = request.user
    player = Player_info.objects.filter(username=user).first()
    
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
        "skill_points": player.skill_points
        
        
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



