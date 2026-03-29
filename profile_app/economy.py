from .models import Player_info

def gold_plus(user, amount):
    print(f"Funkce gold_plus byla zavolána s uživatelem: {user} a množstvím zlata: {amount}")
    player = Player_info.objects.filter(username=user).first()
    if player:
        print(f"Stávající množství zlata pro uživatele {user}: {player.gold}")
        player.gold += float(amount)
        player.save()
        print(f"Nové množství zlata pro uživatele {user}: {player.gold}")

        return True
    return False