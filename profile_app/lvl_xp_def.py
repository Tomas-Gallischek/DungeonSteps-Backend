
def xp_plus(player_info, xp_amount):
    print(f"Funkce xp_plus: Přidávám {xp_amount} XP hráči {player_info.username}")
    player_info.xp += xp_amount

    
    player_info.save()