from .models import Player_info


def atr_up(user, atr_name):    
    user = Player_info.objects.filter(username=user).first()
    user_name = user.username
    atr_name = atr_name.lower()
    

    
    if atr_name == 'str':
        user.str_stats += 1
    elif atr_name == 'dex':
        user.dex_stats += 1
    elif atr_name == 'int':
        user.int_stats += 1
    elif atr_name == 'vit':
        user.vit_stats += 1
    elif atr_name == 'luck':
        user.luck_stats += 1
    else:
        # Pokud přijde nějaký nesmyslný text
        return False
    
    user.atr_points -= 1
    user.save()
    
    atr_max_update(user_name)
    
    return True


def atr_max_update(user_name):
    user = Player_info.objects.filter(username=user_name).first()
    
    all_atr = ['str', 'dex', 'int', 'vit', 'luck']
    
    for atr in all_atr:
        base_value = getattr(user, f"{atr}_base")
        stats_value = getattr(user, f"{atr}_stats")
        eqp_value = getattr(user, f"{atr}_eqp")
        max_value = base_value + stats_value + eqp_value
        setattr(user, f"{atr}_max", max_value)
        user.save()