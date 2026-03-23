from rest_framework.response import Response
from rest_framework import status
from profile_app.models import Player_info
from enemy_app.models import Enemy


def fight(player, enemy_init_name):
    print ("Funkce fight byla zavolána!")
    
# INICIALIZACE
    player = Player_info.objects.filter(username=player).first()
    enemy = Enemy.objects.filter(init_name=enemy_init_name).first()
    
    if not enemy:
        return Response({"error": "Nepřítel nenalezen"}, status=status.HTTP_404_NOT_FOUND)
    
    
    
    
    
    winner = player.username    
    
    result = winner
       
    return result



# SOUBOJOVÁ LOGIKA:

# 1) Načtení obou stran

# 2) Porovnání atributů (síla, obratnost, inteligence)