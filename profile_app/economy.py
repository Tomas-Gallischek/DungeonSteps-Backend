from .models import Player_info

def gold_plus(user, amount):

    player = Player_info.objects.filter(username=user).first()
    if player:
        player.gold += amount
        player.save()
        return True
    return False