from django.db import models


class Item_default(models.Model):
    CATEGORY_CHOICES = [
        ('weapon', 'Weapon'),
        ('armor', 'Armor'),
        ('helmet', 'Helmet'),
        ('boots', 'Boots'),
        ('amulet', 'Amulet'),
        ('ring', 'Ring'),
        ('talisman', 'Talisman'),
        ('pet', 'Pet'),
        ('material', 'Material'),
        ('useable', 'Useable'),
        ('other', 'Other'),
    ]
    
    RARITY_CHOICES = [
    ('common', 'Common'),
    ('rare', 'Rare'),
    ('epic', 'Epic'),
    ('legendary', 'Legendary'),
]
    
    name = models.CharField(max_length=100)
    item_img_ozn = models.CharField(default='dopln_nazev_obrazku_bez_png', max_length=100, blank=True, null=True)
    item_base_id = models.IntegerField(unique=True, blank=True, null=True) # unikátní ID pro každý základní item, slouží k identifikaci při generování a upgradu
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    lvl_req = models.IntegerField(null=True, blank=True, default=1)
    shop_max_lvl_drop = models.IntegerField(null=True, blank=True, default=99)
    specific_rarity = models.CharField(max_length=50, choices=RARITY_CHOICES, blank=True, null=True, default=None) # pro specifické itemy, které mají pevnou raritu (např. legendární peti)
    stack_able = models.BooleanField(default=True)
    item_lvl = models.IntegerField(default=0, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.category} - Base ID: {self.item_base_id}"
    
    class Meta:
        verbose_name = "--- VŠECHNY ITEMY ---"
        verbose_name_plural = "--- VŠECHNY ITEMY ---"

    # SEŘAZENÍ PODLE BASE_ID KDYŽ NA TUTO DATABÁZI ODKAZUJU
        ordering = ['item_base_id'] 
        # (Pokud bys chtěl sestupně, dáš ['-item_base_id'])

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
    plus_attack_speed = models.FloatField(null=True, blank=True, default=1.0)
    
    # UPGRADE
    weapon_dmg_up_koef = models.FloatField(null=True, blank=True, default=0.08, help_text="Zvyšuje se o tento procento s každou úrovní (např. 0.08 = 8%)")
    
    def __str__(self):
        return f"{self.item.name} - {self.dmg_type} - {self.dmg_base} - {self.plus_attack_speed} - Weapon Details"
    
    class Meta:
        verbose_name = "Weapon Submodel"
        verbose_name_plural = "Weapon Submodels"
    
class Item_Armor_Submodel(models.Model):
    DMG_TYPE_CHOICES = [
    ('heavy', 'Heavy'),
    ('light', 'Light'),
    ('magic', 'Magic'),
    ('none', 'None'),
]
    item = models.OneToOneField(Item_default, on_delete=models.CASCADE, related_name='armor_details')
    dmg_type = models.CharField(max_length=50, choices=DMG_TYPE_CHOICES, default='none')   
    armor_base = models.IntegerField(null=True, blank=True)
    plus_hp = models.IntegerField(null=True, blank=True)
    min_minus_attack_speed = models.FloatField(null=True, blank=True, default=0.01)
    max_minus_attack_speed = models.FloatField(null=True, blank=True, default=0.05) 
    
    
    # UPGRADE
    armor_armor_up_koef = models.FloatField(null=True, blank=True, default=0.1, help_text="Zvyšuje se o tento procento s každou úrovní (např. 0.1 = 10%)")
    armor_hp_up_koef = models.FloatField(null=True, blank=True, default=0.1, help_text="Zvyšuje se o tento procento s každou úrovní (např. 0.1 = 10%)")
    
    def __str__(self):
        return f"{self.item.name} - {self.dmg_type} - {self.armor_base} - {self.min_minus_attack_speed} - {self.max_minus_attack_speed} - {self.plus_hp} - Armor Details"
    
    class Meta:
        verbose_name = "Armor Submodel"
        verbose_name_plural = "Armor Submodels"
class Item_Helmet_Submodel(models.Model):    
    DMG_TYPE_CHOICES = [
    ('heavy', 'Heavy'),
    ('light', 'Light'),
    ('magic', 'Magic'),
    ('none', 'None'),
]
    
    item = models.OneToOneField(Item_default, on_delete=models.CASCADE, related_name='helmet_details')
    dmg_type = models.CharField(max_length=50, choices=DMG_TYPE_CHOICES, default='none')   
    armor_base = models.IntegerField(null=True, blank=True)
    min_minus_attack_speed = models.FloatField(null=True, blank=True, default=0.0)
    max_minus_attack_speed = models.FloatField(null=True, blank=True, default=0.0)
    
    
    # UPGRADE
    helmet_armor_up_koef = models.FloatField(null=True, blank=True, default=0.1, help_text="Zvyšuje se o tento procento s každou úrovní (např. 0.1 = 10%)")
    
    def __str__(self):
        return f"{self.item.name} - {self.dmg_type} - {self.armor_base} - {self.min_minus_attack_speed} - {self.max_minus_attack_speed} - Helmet Details"
    
    class Meta:
        verbose_name = "Helmet Submodel"
        verbose_name_plural = "Helmet Submodels"
    
class Item_Boots_Submodel(models.Model):
    DMG_TYPE_CHOICES = [
    ('heavy', 'Heavy'),
    ('light', 'Light'),
    ('magic', 'Magic'),
    ('none', 'None'),
]
    item = models.OneToOneField(Item_default, on_delete=models.CASCADE, related_name='boots_details')
    dmg_type = models.CharField(max_length=50, choices=DMG_TYPE_CHOICES, default='none')
    armor_base = models.IntegerField(null=True, blank=True)
    plus_percent_attack_speed = models.FloatField(null=True, blank=True, default=0.0)
    
    # UPGRADE
    boots_armor_up_koef = models.FloatField(null=True, blank=True, default=0.1, help_text="Zvyšuje se o tento procento s každou úrovní (např. 0.1 = 10%)")
    boots_attack_speed_up_koef = models.FloatField(null=True, blank=True, default=0.1, help_text="Zvyšuje se o tento procento s každou úrovní (např. 0.1 = 10%)")  
    
    def __str__(self):
        return f"{self.item.name} - {self.dmg_type} - {self.armor_base} - {self.plus_percent_attack_speed} - Boots Details"    
    
    class Meta:
        verbose_name = "Boots Submodel"
        verbose_name_plural = "Boots Submodels"
    
class Item_Amulet_Submodel(models.Model):
    item = models.OneToOneField(Item_default, on_delete=models.CASCADE, related_name='amulet_details')   
    all_atr_bonus = models.FloatField(null=True, blank=True, default=0.0)
    
    # UPGRADE
    amulet_atr_up_koef = models.FloatField(null=True, blank=True, default=0.2, help_text="Zvyšuje se o tento procento s každou úrovní (např. 0.2 = 20%)")
        
    def __str__(self):
        return f"{self.item.name} - {self.all_atr_bonus} - Amulet Details"
    
    class Meta:
        verbose_name = "Amulet Submodel"
        verbose_name_plural = "Amulet Submodels"
    
class Item_Ring_Submodel(models.Model):
    item = models.OneToOneField(Item_default, on_delete=models.CASCADE, related_name='ring_details')   
    all_atr_bonus = models.FloatField(null=True, blank=True, default=0.0)
     
    # UPGRADE
    ring_atr_up_koef = models.FloatField(null=True, blank=True, default=0.2, help_text="Zvyšuje se o tento procento s každou úrovní (např. 0.2 = 20%)")
        
    def __str__(self):
        return f"{self.item.name} - {self.all_atr_bonus} - Ring Details"
    
    class Meta:
        verbose_name = "Ring Submodel"
        verbose_name_plural = "Ring Submodels"
    
class Item_Talisman_Submodel(models.Model):
    item = models.OneToOneField(Item_default, on_delete=models.CASCADE, related_name='talisman_details')   
    
# BONUS TALISMANU SE GENERUJE AŽ NA ÚROVNI HRÁČE
        
    def __str__(self):
        return f"{self.item.name} - Talisman Details"
    
    class Meta:
        verbose_name = "Talisman Submodel"
        verbose_name_plural = "Talisman Submodels"
    
    
    
class Item_Pet_Submodel(models.Model):
    item = models.OneToOneField(Item_default, on_delete=models.CASCADE, related_name='pet_details')
    min_pet_lvl = models.IntegerField(null=True, blank=True, default=1)   
    max_pet_lvl = models.IntegerField(null=True, blank=True, default=100)
    
    min_armor_bonus = models.FloatField(null=True, blank=True, default=0.5)
    max_armor_bonus = models.FloatField(null=True, blank=True, default=5.0)
    
    min_dmg_bonus = models.FloatField(null=True, blank=True, default=1.0)
    max_dmg_bonus = models.FloatField(null=True, blank=True, default=5.0)
    
    min_hp_bonus = models.FloatField(null=True, blank=True, default=2.0)
    max_hp_bonus = models.FloatField(null=True, blank=True, default=20.0)

    min_prum_skoda_bonus = models.FloatField(null=True, blank=True, default=0.1)
    max_prum_skoda_bonus = models.FloatField(null=True, blank=True, default=0.5)
    
    def __str__(self):
        return f"{self.item.name} - Pet Details"
    
    class Meta:
        verbose_name = "Pet Submodel"
        verbose_name_plural = "Pet Submodels"    

class Item_Material_Submodel(models.Model):
    
    TYPE_CHOICES = [
        ('upgrade', 'Upgrade'),
        ('crafting', 'Crafting'),
        ('food', 'Food'),
        ('quest', 'Quest'),
        ('rune', 'Rune'),
        ('useable', 'Useable'),
        ('spell', 'Spell'),
        ('other', 'Other'),
    ]
    
    RARITY_CHOICES = [
    ('common', 'Common'),
    ('rare', 'Rare'),
    ('epic', 'Epic'),
    ('legendary', 'Legendary'),
]
    
    item = models.OneToOneField(Item_default, on_delete=models.CASCADE, related_name='material_details')   
    material_type = models.CharField(max_length=50, blank=True, null=True, choices=TYPE_CHOICES, default='upgrade')
    rarity = models.CharField(max_length=50, blank=True, null=True, choices=RARITY_CHOICES, default='common')
    price_ks = models.FloatField(blank=True, null=True, default=1)
    
    def __str__(self):
        return f"{self.item.name} - {self.material_type} - {self.rarity} - {self.price_ks} - Material Details"

    class Meta:
        verbose_name = "Material Submodel"
        verbose_name_plural = "Material Submodels"

class All_Items_Bonus(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True) # název bonusu, např. "Strength Bonus", "Agility Bonus", atd.
    description = models.TextField(max_length=500, blank=True, null=True) # popis bonusu
    bonus_type = models.CharField(max_length=50, blank=True, null=True) # typ bonusu, např. "strength", "agility", "intellect", "hp", "mp", atd.
    min_value = models.FloatField(blank=True, null=True) # minimální hodnota bonusu
    max_value = models.FloatField(blank=True, null=True) # maximální hodnota bonusu
    
    def __str__(self):
        return f"{self.name} - {self.bonus_type}: {self.min_value} - {self.max_value}" 


    class Meta:
        verbose_name = "All Items Bonus"
        verbose_name_plural = "All Items Bonuses"
        
        
class ItemUpgrade(models.Model):
    """Jeden záznam = jeden konkrétní level vylepšení pro daný předmět."""
    item = models.ForeignKey(Item_default, on_delete=models.CASCADE, related_name='upgrades')
    lvl = models.PositiveIntegerField() # Např. 1, 2, 3...
    gold_cost = models.PositiveIntegerField(default=0, help_text="AUTOMATICKY doplněno")
    delfault_chance = models.BooleanField(default=True, help_text="Základní nastavení (50% / lvl10)")
    custom_chance = models.BooleanField(default=False, help_text="Použít vlastní šanci místo základní")
    
    chance = models.FloatField(null=True, blank=True, help_text="0.1 = 10%, 1=100% - AUTO DOPLNĚNÍ při DEFAULT_CHANCE = TRUE")

    class Meta:
        # Zabrání tomu, abys omylem vytvořil dvě různá vylepšení na level 2 pro stejný item
        unique_together = ('item', 'lvl')
        ordering = ['lvl']

    def save(self, *args, **kwargs):
        
    # AUTOMATICKÉ DOPLNĚNÍ CENY
        lvl_koef = 5
        up_koef = 1.5
        lvl_req = self.item.lvl_req if self.item.lvl_req else 1
        
        final_cost = (lvl_koef * (lvl_req * lvl_req))
        
        for lvl in range(1, self.lvl + 1):
            final_cost *= up_koef
            
        self.gold_cost = round(final_cost)
        
    # AUTOMATICKÉ DOPLNĚNÍ ŠANCE
        if self.delfault_chance:
            base_chance = 0.95
            chance_decrease_per_level = 0.05
            
            calculated_chance = round(base_chance - (chance_decrease_per_level * (self.lvl - 1)), 2)
            self.chance = max(calculated_chance, 0.01)  # Zajistí, že šance nikdy neklesne pod 1%
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.name} - Upgrade na Lvl {self.lvl} - Cena: {self.gold_cost} g"


class UpgradeMaterial(models.Model):
    """Tohle řeší ten problém s množstvím! Kolik kterého materiálu je potřeba."""
    upgrade = models.ForeignKey(ItemUpgrade, on_delete=models.CASCADE, related_name='materials')
    material = models.ForeignKey(Item_default, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.amount}x {self.material.name} pro {self.upgrade}"
    

    
    
    