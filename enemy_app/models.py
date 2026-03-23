from django.db import models

class Enemy(models.Model):
    
    CATEGORY_CHOICES = [
        ('Boss', 'Boss'),
        ('Void', 'Void'),
        ('Mob', 'Mob'),
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
    
    
    armor = models.IntegerField(blank=True, null=True)
    dmg_min = models.IntegerField(blank=True, null=True)
    dmg_max = models.IntegerField(blank=True, null=True)
    attack_speed = models.FloatField(blank=True, null=True)
    critical_chance = models.FloatField(blank=True, null=True)
    critical_multiplier = models.FloatField(blank=True, null=True)
    
# OSTATNÍ
    loot = models.JSONField(blank=True, null=True)


    

    def __str__(self):
        return self.name
