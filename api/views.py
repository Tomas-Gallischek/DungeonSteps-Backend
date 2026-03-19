from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status
from profile_app.models import Player_info


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


@api_view(['GET'])
def test_spojeni(request):
    # Tento slovník se automaticky převede na formát JSON
    data = {
        "status": "success",
        "message": "Ahoj! Backend a frontend spolu úspěšně komunikují."
    }
    return Response(data)



# Tato třída zajistí, že login bude vždy dostupný a bude vracet Token
class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]
    
    

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