from rest_framework.response import Response
from rest_framework import status
import random
from .loot import loot_generator, loot_gold_generator

def fight(player, enemy, wave):
    turn_logs = []
    all_loot_obtained = []
    all_gold_obtained = []
    
    if not player or not enemy:
        return Response({"error": "Player or Enemy not found."}, status=status.HTTP_404_NOT_FOUND)

    p_img = player.avatar_img_ozn
    e_img = enemy.enemy_img_ozn
    p_actual_hp = player.hp_max
    e_actual_hp = enemy.hp_max
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
            if e_actual_hp < 0:
                e_actual_hp = 0
                event_type = "enemy_defeated"
            else:
                event_type = "player_attack"
            
            p_next_attack += p_speed
            if e_actual_hp <= 0:
                winner = player.username
                print(f"{player.username} has defeated {enemy.name}!")
                
                all_loot_obtained.extend(loot_generator(player=player, enemy=enemy))
                all_gold_obtained.extend(loot_gold_generator(enemy=enemy))
                
            get_turn_logs(current_time, enemy.name, player.username, e_actual_hp, p_actual_hp, p_damage_dealt, turn_logs, p_damage_status, enemy.hp_max, player.hp_max, True, False, p_img, e_img, wave, event_type, all_loot_obtained, all_gold_obtained)
            if e_actual_hp <= 0:
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
            if p_actual_hp < 0:
                p_actual_hp = 0
                event_type = "player_defeated"
            else:
                event_type = "enemy_attack"
            
            e_next_attack += e_speed
            if p_actual_hp <= 0:
                winner = enemy.name
                print(f"{enemy.name} has defeated {player.username}!")

            get_turn_logs(current_time, player.username, enemy.name, p_actual_hp, e_actual_hp, e_damage_dealt, turn_logs, e_damage_status, player.hp_max, enemy.hp_max, False, True, p_img, e_img, wave, event_type, all_loot_obtained, all_gold_obtained)

            if p_actual_hp <= 0:
                break
    
    return current_time, enemy.id_unique, turn_logs, winner, all_loot_obtained, all_gold_obtained


def get_turn_logs(
    current_time,
    defender,
    attacker,
    defender_actual_hp,
    attacker_actual_hp,
    damage_dealt,
    turn_logs,
    damage_status,
    defender_max_hp,
    attacker_max_hp,
    is_attacker_player,
    is_attacker_enemy,
    player_img,
    enemy_img,
    wave,
    event_type,
    all_loot_obtained,
    all_gold_obtained
):

        turn_logs.extend([{
        "time_offset": round(current_time, 2),
        "is_attacker_player": bool(is_attacker_player),
        "is_attacker_enemy": bool(is_attacker_enemy),
        "attacker": str(attacker),
        "defender": str(defender),
        "damage": damage_dealt,
        "damage_status": str(damage_status),
        "defender_max_hp": defender_max_hp,
        "attacker_max_hp": attacker_max_hp,
        "defender_hp": max(0, defender_actual_hp),
        "attacker_hp": max(0, attacker_actual_hp),
        "player_img": str(player_img),
        "enemy_img": str(enemy_img),
        "wave": int(wave),
        "event_type": str(event_type), # "player_attack", "enemy_attack", "enemy_defeated", "player_defeated"
        "loot_dropped": [{
                "name": item["name"],
                "amount": item["amount"],
            } for item in all_loot_obtained
        ],
        "gold_dropped": sum(all_gold_obtained)
    }])
        
    
        
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
    
    