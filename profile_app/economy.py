from .models import Player_info

def gold_plus(user, amount):
    player = Player_info.objects.filter(username=user.username).first()
    player.gold += amount
    player.save()
    return True
    