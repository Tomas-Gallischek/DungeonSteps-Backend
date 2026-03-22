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


@api_view(['POST'])
@permission_classes([AllowAny]) # Registrace musí být přístupná všem
def registrace(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response({"error": "Chybí jméno nebo heslo"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Uživatel již existuje"}, status=status.HTTP_400_BAD_REQUEST)

    # Vytvoření uživatele (Django automaticky hash hesla)
    user = User.objects.create_user(username=username, password=password, email=email)
    
    # Vytvoření profilu hráče
    Player_info.objects.create(username=user)
    
    
    # Vytvoření tokenu pro okamžité přihlášení po registraci
    token = Token.objects.create(user=user)
    
    return Response({"token": token.key, "message": "Registrace proběhla úspěšně"}, status=status.HTTP_201_CREATED)
    
    

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




@api_view(['POST'])
@permission_classes([IsAuthenticated]) # Tady ZAMYKÁME endpoint jen pro přihlášené!
def admin_plus_gold(request):
    print("Funkce admin_plus_gold byla zavolána!")
    hrac = request.user # identifikace přihlášeného uživatele
    amount = request.data.get('amount') # očekáváme, že frontend nám pošle množství zlata, které chceme přidat

    try:
        amount = int(amount)
    except (TypeError, ValueError):
        return Response({"error": "Parametr 'amount' musí být celé číslo"}, status=status.HTTP_400_BAD_REQUEST)

    if amount <= 0:
        return Response({"error": "Parametr 'amount' musí být kladné číslo"}, status=status.HTTP_400_BAD_REQUEST)

    gold_plus(user=hrac, amount=amount) # zavoláme funkci z economy.py, která přidá zlato hráči

    return Response({"message": f"Úspěšně odesláno: {amount} zlata pro hráče {hrac.username}"}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_plus_xp(request):
    print("Funkce admin_plus_xp byla zavolána!")
    hrac = request.user 
    mnozstvi = request.data.get('mnozstvi') # Frontend (Kivy) posílá parametr 'mnozstvi'

    try:
        mnozstvi = int(mnozstvi)
    except (TypeError, ValueError):
        return Response({"error": "Parametr 'mnozstvi' musí být celé číslo"}, status=status.HTTP_400_BAD_REQUEST)

    if mnozstvi <= 0:
        return Response({"error": "Parametr 'mnozstvi' musí být kladné číslo"}, status=status.HTTP_400_BAD_REQUEST)

    # Najdeme profil hráče podle jména, pokud chybí tak ho vytvoříme
    profil, _ = Player_info.objects.get_or_create(username=hrac)

    # Zavoláme tvoji připravenou funkci z lvl_xp_def.py
    xp_plus(player_info=profil, xp_amount=mnozstvi)

    return Response({"message": f"Úspěšně odesláno: {mnozstvi} XP pro hráče {hrac.username}"}, status=status.HTTP_200_OK)