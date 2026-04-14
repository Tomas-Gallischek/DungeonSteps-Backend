from .models import Player_info

def xp_plus(user, xp_amount):
    print(f"Funkce xp_plus byla zavolána s uživatelem: {user} a množstvím XP: {xp_amount}")
    player = Player_info.objects.filter(username=user).first()

    if player:
        player.xp += xp_amount
        player.save()
        while player.xp >= player.xp_next_lvl:
            lvl_up(player)



def lvl_up(player):
    print(f"Funkce lvl_up byla zavolána pro hráče: {player.username}")
    
    # zvednutí levelu
    player.lvl += 1
    player.xp -= player.xp_next_lvl
    
    xp_var = 1.01
    for i in range (1, player.lvl):
        xp_var += 0.001
        if xp_var >= 1.05:
            xp_var = 1.05
        print(f"Level: {i} | XP Var: {xp_var:.3f}")
            
    new_xp = player.xp_next_lvl * xp_var
    
    player.xp_next_lvl = float(new_xp)  # Zvyšování XP pro další úroveň O 10% každou úroveň
    
    # ATRIBUT A SKILL POINTS
    player.atr_points += 5
    player.skill_points += 1
    print(f"Přidány atributové body: {player.atr_points}, skill body: {player.skill_points}")
    
    player.save()