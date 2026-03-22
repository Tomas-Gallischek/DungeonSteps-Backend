from django.db import models
from django.core.validators import MinValueValidator


class Player_info(models.Model):
    
# ZÁKLADNÍ INFORMACE
    username = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    lvl = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    xp = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    xp_next_lvl = models.IntegerField(default=8000, validators=[MinValueValidator(1)])
    gold = models.IntegerField(default=0, validators=[MinValueValidator(0)])

# POINTS
    atr_points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    skill_points = models.IntegerField(default=0, validators=[MinValueValidator(0)])

# KROKY
    steps = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    steps_today = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
# ATRIBUTY
    str_base = models.IntegerField(default=1, blank=True)
    str_stats = models.IntegerField(default=0, blank=True)
    str_eqp = models.IntegerField(default=0, blank=True)
    str_max = models.IntegerField(default=1, blank=True)
    
    dex_base = models.IntegerField(default=1, blank=True)
    dex_stats = models.IntegerField(default=0, blank=True)
    dex_eqp = models.IntegerField(default=0, blank=True)
    dex_max = models.IntegerField(default=1, blank=True)
    
    int_base = models.IntegerField(default=1, blank=True)
    int_stats = models.IntegerField(default=0, blank=True)
    int_eqp = models.IntegerField(default=0, blank=True)
    int_max = models.IntegerField(default=1, blank=True)    

    vit_base = models.IntegerField(default=1, blank=True)
    vit_stats = models.IntegerField(default=0, blank=True)
    vit_eqp = models.IntegerField(default=0, blank=True)
    vit_max = models.IntegerField(default=1, blank=True)
    
    luck_base= models.IntegerField(default=1, blank=True)
    luck_stats = models.IntegerField(default=0, blank=True)
    luck_eqp = models.IntegerField(default=0, blank=True)
    luck_max = models.IntegerField(default=1, blank=True)
    
# BOJ
    hp = models.IntegerField(default=50, blank=True)
    attack_number = models.IntegerField(default=1, blank=True)
    attack_speed = models.FloatField(default=1, blank=True)
    defence_number = models.IntegerField(default=1, blank=True)   
    crit_chance = models.FloatField(default=0, blank=True)
    crit_multiplier = models.FloatField(default=1.5, blank=True) 

    def __str__(self):
        return f"{self.username} - lvl: {self.lvl} - xp: {self.xp} - gold: {self.gold}"