from .models import Player_info

def gold_plus(user, amount):
    print(f"Funkce gold_plus byla zavolána s uživatelem: {user} a množstvím zlata: {amount}")
    player = Player_info.objects.filter(username=user).first()
    if player:
        player.gold += amount
        player.save()
        return True
    return False