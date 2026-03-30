from django.db import models


class Item_default(models.Model):
    CATEGORY_CHOICES = [
        ('weapon', 'Weapon'),
        ('armor', 'Armor'),
        ('material', 'Material'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    item_img_ozn = models.CharField(default='item_default', max_length=100, blank=True, null=True)
    item_base_id = models.IntegerField(unique=True, blank=True, null=True) # unikátní ID pro každý základní item, slouží k identifikaci při generování a upgradu
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    lvl_req = models.IntegerField(null=True, blank=True)
    lvl_max_req = models.IntegerField(null=True, blank=True)
    
    stack_able = models.BooleanField(default=True)
    max_stack = models.IntegerField(blank=True, null=True, default=50)
    
    def __str__(self):
        return f"{self.name} - {self.category} - Base ID: {self.item_base_id}"

class Item_Weapon_Submodel(models.Model):
    DMG_TYPE_CHOICES = [
    ('heavy', 'Heavy'),
    ('light', 'Light'),
    ('magic', 'Magic'),
    ('none', 'None'),
]

    item = models.OneToOneField(Item_default, on_delete=models.CASCADE, related_name='weapon_details')
    dmg_type = models.CharField(max_length=50, choices=DMG_TYPE_CHOICES)
    dmg_base = models.IntegerField(null=True, blank=True)  
    
class Item_Armor_Submodel(models.Model):
    item = models.OneToOneField(Item_default, on_delete=models.CASCADE, related_name='armor_details')   
    armor_base = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.item.name} - Armor Details"
    
class Item_Material_Submodel(models.Model):
    
    TYPE_CHOICES = [
        ('upgrade', 'Upgrade'),
        ('crafting', 'Crafting'),
        ('other', 'Other'),
    ]
    
    RARITY_CHOICES = [
    ('common', 'Common'),
    ('rare', 'Rare'),
    ('epic', 'Epic'),
    ('legendary', 'Legendary'),
]
    
    item = models.OneToOneField(Item_default, on_delete=models.CASCADE, related_name='material_details')   
    material_type = models.CharField(max_length=50, blank=True, null=True, choices=TYPE_CHOICES)
    rarity = models.CharField(max_length=50, blank=True, null=True, choices=RARITY_CHOICES)
    price_ks = models.FloatField(blank=True, null=True, default=1)
    
    def __str__(self):
        return f"{self.item.name} - Material Details"


class All_Items_Bonus(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True) # název bonusu, např. "Strength Bonus", "Agility Bonus", atd.
    description = models.TextField(max_length=500, blank=True, null=True) # popis bonusu
    bonus_type = models.CharField(max_length=50, blank=True, null=True) # typ bonusu, např. "strength", "agility", "intellect", "hp", "mp", atd.
    min_value = models.FloatField(blank=True, null=True) # minimální hodnota bonusu
    max_value = models.FloatField(blank=True, null=True) # maximální hodnota bonusu
    
    def __str__(self):
        return f"{self.name} - {self.bonus_type}: {self.min_value} - {self.max_value}" 

