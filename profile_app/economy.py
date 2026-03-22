from .models import Player_info


def gold_plus(user, amount):
    print(f"Funkce gold_plus byla zavolána s uživatelem: {user} a množstvím: {amount}")
    user = Player_info.objects.get(username=user)
    try:
        user.gold += amount
        user.save()
        return True
    except Player_info.DoesNotExist:
        return False
    