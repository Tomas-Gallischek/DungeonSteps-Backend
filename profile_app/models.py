from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Player_info(models.Model):
    
    ROLE_CHOICES = [
        ('warrior', 'Válečník'),
        ('mage', 'Mág'),
        ('hunter', 'Hraničář'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Muž'),
        ('female', 'Žena'),
        ('other', 'Jiné'),
    ]
    
# ZÁKLADNÍ INFORMACE
    username = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=None, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=None, null=True, blank=True)
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
    dmg_atr = models.CharField(max_length=20, default='none') # Typ poškození, který se bude počítat z atributů a vybavení, může být 'heavy', 'light', 'magic' nebo 'none'
    dmg_atr_value = models.IntegerField(default=1, blank=True, null=True) # Hodnota atributu, který se bude počítat do poškození, může být str, dex nebo int, podle role a vybavení

    hp_base = models.IntegerField(default=0, blank=True)
    hp_stats = models.IntegerField(default=0, blank=True)
    hp_lvl = models.IntegerField(default=0, blank=True)
    hp_eqp = models.IntegerField(default=0, blank=True)
    hp_max = models.IntegerField(default=0, blank=True)
    
    hp_vit_koef = models.IntegerField(("HP Vitality Coefficient"), default=1, blank=True)  # Koeficient pro výpočet HP z vitality
    hp_lvl_koef = models.IntegerField(("HP Level Coefficient"), default=10, blank=True)  # Koeficient pro výpočet HP z úrovně

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

    dmg_base = models.IntegerField(default=1, blank=True) # <-- Základní poškození, které se bude upravovat podle atributů a vybavení
    dmg_avg = models.IntegerField(default=2, blank=True)
    dmg_min = models.IntegerField(default=1, blank=True)
    dmg_max = models.IntegerField(default=3, blank=True)
    
    hp_actual = models.IntegerField(default=1, blank=True) # <-- Aktuální HP, které se mění během boje, ale neovlivňuje max HP
    
    attack_speed = models.FloatField(default=1, blank=True)
    defence_number = models.IntegerField(default=1, blank=True)   
    crit_chance = models.FloatField(default=0, blank=True)
    crit_multiplier = models.FloatField(default=1.5, blank=True) 
    
# EQP
    weapon = models.BooleanField(("Weapon Equipped"), default=False,)
    armor = models.BooleanField(("Armor Equipped"), default=False,)

    def __str__(self):
        return f"{self.username} - lvl: {self.lvl} - xp: {self.xp} - gold: {self.gold}"
    
    

class Player_Items(models.Model):
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
    
    STATUS_CHOICES = [
        ('equipped', 'Equipped'),
        ('inventary', 'Inventory'),
        ('shop', 'Shop'),
        ('drop', 'Drop'),
        ('none', 'None'),
        ('sold', 'Sold'), # TOTO POTÉ NASTAVIT NA UTOMATICKÉ PROMAZÁVÁNÍ, JE TO JEN POJISTKA
    ]
    
    RARITY_CHOICES = [
        ('common', 'Common'),
        ('rare', 'Rare'),
        ('epic', 'Epic'),
        ('legendary', 'Legendary'),
    ]
    
    player = models.ForeignKey(Player_info, on_delete=models.CASCADE, related_name='items')
    item_id = models.AutoField(primary_key=True, unique=True)
    item_base_id = models.IntegerField(blank=True, null=True) # odkaz na základní item pro případ upgradu a generování, může být null pro unikátní předměty vytvořené jen pro hráče
    item_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='none')
    

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    dmg_type = models.CharField(max_length=50, choices=DMG_TYPE_CHOICES)
    lvl_req = models.IntegerField(null=True, blank=True)
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES)
    price = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1)])
    
    dmg_min = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    dmg_max = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    dmg_avg = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    
    armor = models.IntegerField(null=True, blank=True)
    
    
    drop_lvl_min = models.IntegerField(null=True, blank=True)
    drop_lvl_max = models.IntegerField(null=True, blank=True)
    drop_rate = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    item_bonus = models.JSONField(default=dict)  # Ukládá bonusy z předmětu jako JSON


    def __str__(self):
        return f"{self.name} (ID: {self.item_id}) - {self.category} - {self.rarity} - Status: {self.item_status}"
