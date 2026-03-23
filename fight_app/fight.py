from rest_framework.response import Response
from rest_framework import status
from profile_app.models import Player_info
from enemy_app.models import Enemy
import random
from django.utils import timezone
from .models import fight_log

def fight(player, enemy_init_name):
    turn_logs = []
    player = Player_info.objects.filter(username=player).first()
    enemy = Enemy.objects.filter(init_name=enemy_init_name).first()
    time_start = timezone.now()
    print(f"Čas zahájení souboje: {time_start}")
    
    if not player or not enemy:
        return Response({"error": "Player or Enemy not found."}, status=status.HTTP_404_NOT_FOUND)

    p_actual_hp = player.hp_max
    e_actual_hp = enemy.hp
    p_speed = float(player.attack_speed)
    e_speed = float(enemy.attack_speed)
    
    # Kdy proběhne první útok?
    p_next_attack = p_speed
    e_next_attack = e_speed

    # --- SOUBOJ ---
    while e_actual_hp > 0 and p_actual_hp > 0:
        current_time = min(p_next_attack, e_next_attack)
        
        # --- HRÁČ ---
        
        # --- ÚTOK ---
        if current_time == p_next_attack:
            p_dmg = random.randint(player.dmg_min, player.dmg_max)
            p_dmg, p_damage_status = critical_hit(player.crit_chance, player.crit_multiplier, p_dmg)
        
        # --- OBRANA ---
            armor = enemy.armor
            if player.dmg_atr == "str":
                resist_value = enemy.str_resist
            elif player.dmg_atr == "dex":
                resist_value = enemy.dex_resist
            elif player.dmg_atr == "int":
                resist_value = enemy.int_resist
            else:
                resist_value = 0
            armor = resist(armor, resist_value)
            
        # --- SOUČET ---
            p_damage_dealt = max(0, p_dmg - armor)
        
        # --- KONEC ZÁPASU A ZÁPIS DO DATABÁZE ---
            e_actual_hp -= p_damage_dealt
            get_fight_logs(current_time, enemy.name, player.username, e_actual_hp, p_actual_hp, p_damage_dealt, turn_logs, p_damage_status) 
            p_next_attack += p_speed
            if e_actual_hp <= 0:
                winner = player.username
                print(f"{player.username} has defeated {enemy.name}!")
                break

        # --- ENEMY ---
        
        # --- ÚTOK---
        if current_time == e_next_attack:
            e_dmg = random.randint(enemy.dmg_min, enemy.dmg_max)
            e_dmg, e_damage_status = critical_hit(enemy.crit_chance, enemy.crit_multiplier, e_dmg)
            
        # --- OBRANA ---
            armor = player.armor
            if enemy.dmg_atr == "str":
                resist_value = player.str_resist
            elif enemy.dmg_atr == "dex":
                resist_value = player.dex_resist
            elif enemy.dmg_atr == "int":
                resist_value = player.int_resist
            else:
                resist_value = 0
            armor = resist(armor, resist_value)
        
        # --- SOUČET ---
            e_damage_dealt = max(0, e_dmg - armor)
            
        
        # --- KONEC ZÁPASU A ZÁPIS DO DATABÁZE ---
            p_actual_hp -= e_damage_dealt
            get_fight_logs(current_time, player.username, enemy.name, p_actual_hp, e_actual_hp, e_damage_dealt, turn_logs, e_damage_status) 
            e_next_attack += e_speed
            if p_actual_hp <= 0:
                winner = enemy.name
                print(f"{enemy.name} has defeated {player.username}!")
                break

    # UKONČENÍ SOUBOJE A ULOŽENÍ LOGU
    time_end = timezone.now()
    
    fight_log.objects.create(
        player=player,
        enemy=enemy,
        winner=winner,
        time_start=time_start,
        time_end=time_end,
        turn_logs=turn_logs  # JSON pole s asynchronními tahy a relativními časy
    )
    
    result = winner
    
    return result


def get_fight_logs(current_time, defender, attacker, defender_actual_hp, attacker_actual_hp, damage_dealt, turn_logs, damage_status):

        print(f"Čas: {current_time:.2f}s | Útočník: {attacker} | Obránce: {defender} | Poškození: {damage_dealt} ({damage_status}) | HP obránce: {defender_actual_hp} | HP útočníka: {attacker_actual_hp}")

        turn_logs.append({
        "time_offset": round(current_time, 2),
        "attacker": str(attacker),
        "defender": str(defender),
        "damage": damage_dealt,
        "damage_status": damage_status,
        "defender_hp": max(0, defender_actual_hp),
        "attacker_hp": max(0, attacker_actual_hp)
    })
        
    
        
def critical_hit(chance, multiplayer, dmg):
    
    critic_roll = random.randint(1, 100)
    if critic_roll <= chance:
        dmg = int(dmg * multiplayer)
        dmg_status = "critical"
        return dmg, dmg_status
    else:
        dmg = int(dmg)
        dmg_status = "normal"
        return dmg, dmg_status
    
def resist(armor, resist_value):
    resist = armor * (resist_value / 10)
    armor += int(resist)
    return armor
    
    