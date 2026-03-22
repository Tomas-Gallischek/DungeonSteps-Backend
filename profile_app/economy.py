from .models import Player_info


def gold_plus(user, amount):
    print(f"Funkce gold_plus byla zavolána s uživatelem: {user} a množstvím: {amount}")
    profil, _ = Player_info.objects.get_or_create(username=user)
    profil.gold += amount
    profil.save()
    return True
    