from .models import Player_info


def xp_plus(player_info, xp_amount):
    xp_amount = int(xp_amount)
    xp_old = player_info.xp
    xp_need = player_info.xp_next_lvl
    lvl_actual = player_info.lvl
    
    
    player_info.xp += xp_amount
    
    if player_info.xp >= xp_need:
        player_info.lvl += 1
        player_info.xp = player_info.xp - xp_need
        player_info.xp_next_lvl = int(player_info.xp_next_lvl * 1.1)
    
    player_info.save()