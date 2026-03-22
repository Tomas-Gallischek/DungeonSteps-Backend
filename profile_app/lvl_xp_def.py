from .models import Player_info

def xp_plus(user, xp_amount):
    player = Player_info.objects.filter(username=user.username).first()
    player.xp += xp_amount
    player.save()
    return True
