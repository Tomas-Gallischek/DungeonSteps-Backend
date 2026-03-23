from rest_framework.response import Response
from rest_framework import status
from profile_app.models import Player_info
from enemy_app.models import Enemy
import random
from django.utils import timezone
from .models import fight_log

def fight(player, enemy_init_name):
    print("Funkce fight byla zavolána!")
    
    # INICIALIZACE
    turn_logs = []
    
    # Získání modelů (jméno proměnné v argumentu změněno na player_username pro přehlednost)
    player = Player_info.objects.filter(username=player).first()
    enemy = Enemy.objects.filter(init_name=enemy_init_name).first()
    
    time_start = timezone.now()
    print(f"Čas zahájení souboje: {time_start}")
    
    if not player or not enemy:
        return Response({"error": "Player or Enemy not found."}, status=status.HTTP_404_NOT_FOUND)
    
    # NASTAVENÍ HP:
    p_actual_hp = player.hp_max
    e_actual_hp = enemy.hp

    # NASTAVENÍ RYCHLOSTÍ (převod na float pro jistotu)
    p_speed = float(player.attack_speed)
    e_speed = float(enemy.attack_speed)
    
    # Kdy proběhne první útok? Za čas odpovídající rychlosti zbraně
    p_next_attack = p_speed
    e_next_attack = e_speed

    # SOUBOJ NA ČASOVÉ OSE
    while e_actual_hp > 0 and p_actual_hp > 0:
        
        # Posuneme se v čase k nejbližší události (kdo je na řadě?)
        current_time = min(p_next_attack, e_next_attack)
        
        # --- HRÁČ ÚTOČÍ ---
        if current_time == p_next_attack:
            # random.randint(a, b) zahrnuje i obě krajní hodnoty, nahrazuje choice(range)
            p_base_dmg = random.randint(player.dmg_min, player.dmg_max)
            p_damage_dealt = max(0, p_base_dmg - enemy.armor)
            
            e_actual_hp -= p_damage_dealt
            
            turn_logs.append({
                "time_offset": round(current_time, 2), # Relativní čas (např. 1.2)
                "attacker": str(player.username),
                "defender": str(enemy.name),
                "damage": p_damage_dealt, # Ukládáme jako Int
                "defender_hp": max(0, e_actual_hp), # Aktuální HP po zásahu
                "attacker_hp": p_actual_hp # Aktuální HP hráče pro případ, že by se změnily v průběhu souboje (např. léčení) - pro přehlednost logu
            })
            
            print(f"[{current_time:.2f}s] {player.username} attacks {enemy.name} for {p_damage_dealt} damage. Enemy HP left: {e_actual_hp}")
            
            # Hráč zaútočil, naplánujeme jeho další útok
            p_next_attack += p_speed
            
            if e_actual_hp <= 0:
                winner = player.username
                print(f"{player.username} has defeated {enemy.name}!")
                break

        # --- NEPŘÍTEL ÚTOČÍ ---
        if current_time == e_next_attack:
            e_base_dmg = random.randint(enemy.dmg_min, enemy.dmg_max)
            e_damage_dealt = max(0, e_base_dmg - player.armor)
            
            p_actual_hp -= e_damage_dealt
            
            turn_logs.append({
                "time_offset": round(current_time, 2),
                "attacker": str(enemy.name),
                "defender": str(player.username),
                "damage": e_damage_dealt,
                "defender_hp": max(0, p_actual_hp),
                "attacker_hp": e_actual_hp
            })
            
            print(f"[{current_time:.2f}s] {enemy.name} attacks {player.username} for {e_damage_dealt} damage. Player HP left: {p_actual_hp}")
            
            # Nepřítel zaútočil, naplánujeme jeho další útok
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