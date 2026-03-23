from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Enemy(models.Model):
    
    CATEGORY_CHOICES = [
        ('Boss', 'Boss'),
        ('Void', 'Void'),
        ('Mob', 'Mob'),
    ]
    
    ATR_CHOICES = [
        ('str', 'str'),
        ('dex', 'dex'),
        ('int', 'int'),
    ]  
    
# ZÁKLADNÍ INFO
    id_unique = models.AutoField(primary_key=True)
    id_base = models.IntegerField(unique=True)
    init_name = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    lvl = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True, null=True)
    spawn_option = models.BooleanField(blank=True, null=True)
    
# STATY
    hp = models.IntegerField(blank=True, null=True)
    hp_regen_5s = models.FloatField(blank=True, null=True)
    hp_actual = models.IntegerField(default=1, blank=True) # <-- Aktuální HP, které se mění během boje, ale neovlivňuje max HP
    str_resist = models.FloatField(blank=True, null=True, default=5, validators=[MinValueValidator(0), MaxValueValidator(50)])
    dex_resist = models.FloatField(blank=True, null=True, default=5, validators=[MinValueValidator(0), MaxValueValidator(50)])
    int_resist = models.FloatField(blank=True, null=True, default=5, validators=[MinValueValidator(0), MaxValueValidator(50)])
    armor = models.IntegerField(blank=True, null=True)
    dmg_min = models.IntegerField(blank=True, null=True)
    dmg_max = models.IntegerField(blank=True, null=True)
    dmg_atr = models.CharField(max_length=10, choices=ATR_CHOICES, blank=True, null=True)
    attack_speed = models.FloatField(blank=True, null=True)
    crit_chance = models.FloatField(default = 0,blank=True, null=True)
    crit_multiplier = models.FloatField(default = 1,blank=True, null=True)
    
# OSTATNÍ
    loot = models.JSONField(blank=True, null=True)


    

    def __str__(self):
        return self.name
