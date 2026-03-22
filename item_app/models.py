from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Item_default(models.Model):
    
    # POUZE ZÁKLADNÍ INFORMACE O ITEMECH, BEZ VARIANT A UPGRADŮ 
    
    CATEGORY_CHOICES = [
        ('weapon', 'Weapon'),
        ('armor', 'Armor'),
        ('other', 'Other'),
    ]
    
    DMG_TYPE_CHOICES = [
        ('heavy', 'Heavy'),
        ('light', 'Light'),
        ('magic', 'Magic'),
        ('none', 'None'),
    ]
    
    name = models.CharField(max_length=100)
    item_base_id = models.IntegerField(unique=True, blank=True, null=True) # unikátní ID pro každý základní item, slouží k identifikaci při generování a upgradu
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    dmg_type = models.CharField(max_length=50, choices=DMG_TYPE_CHOICES)
    lvl_req = models.IntegerField(null=True, blank=True)
    
    dmg_base = models.IntegerField(null=True, blank=True) # základní hodnota poškození pro zbraně
    
    armor_base = models.IntegerField(null=True, blank=True) # základní hodnota obrany pro brnění
    
    drop_lvl_min = models.IntegerField(null=True, blank=True)
    drop_lvl_max = models.IntegerField(null=True, blank=True)
    drop_rate = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)]) # 1 = 100% drop rate
    
    

    
    def __str__(self):
        return self.name


class All_Items_Bonus(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True) # název bonusu, např. "Strength Bonus", "Agility Bonus", atd.
    description = models.TextField(max_length=500, blank=True, null=True) # popis bonusu
    bonus_type = models.CharField(max_length=50, blank=True, null=True) # typ bonusu, např. "strength", "agility", "intellect", "hp", "mp", atd.
    min_value = models.FloatField(blank=True, null=True) # minimální hodnota bonusu
    max_value = models.FloatField(blank=True, null=True) # maximální hodnota bonusu
    
    def __str__(self):
        return f"{self.name} - {self.bonus_type}: {self.min_value} - {self.max_value}" 

