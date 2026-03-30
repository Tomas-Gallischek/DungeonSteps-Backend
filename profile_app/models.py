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

# OBRÁZKY
    avatar_img_ozn = models.CharField(default='avatar_default', max_length=100, null=True, blank=True)
    background = models.CharField(default='background_default', max_length=100, null=True, blank=True)

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
    attack_speed = models.FloatField(default=1, blank=True)
    crit_chance = models.FloatField(default=0, blank=True)
    crit_multiplier = models.FloatField(default=1.5, blank=True) 
    
    armor = models.IntegerField(default=1, blank=True)
    hp_actual = models.IntegerField(default=1, blank=True) # <-- Aktuální HP, které se mění během boje, ale neovlivňuje max HP
    dex_resist = models.FloatField(default=0, blank=True, validators=[MaxValueValidator(50)]) # <-- Odolnost proti poškození založenému na obratnosti, která se bude počítat z atributů a vybavení
    int_resist = models.FloatField(default=0, blank=True, validators=[MaxValueValidator(50)]) # <-- Odolnost proti poškození založenému na inteligenci, která se bude počítat z atributů a vybavení
    str_resist = models.FloatField(default=0, blank=True, validators=[MaxValueValidator(50)]) # <-- Odolnost proti poškození založenému na síle, která se bude počítat z atributů a vybavení

    

    def __str__(self):
        return f"{self.username} - lvl: {self.lvl} - xp: {self.xp} - gold: {self.gold}"
    
    
    def save(self, *args, **kwargs):
        
    # PŘI REGISTRACI JE NUTNO PRVNBĚ VŠECHNO ULOŽIT A AŽ PAK SPUSTIT METODU SAVE() ZNOVA
        if self.gender is None or self.role is None:
            super().save(*args, **kwargs)
            return
        
        
    # AKTUALIZACE ATRIBUTŮ
        self.str_max = self.str_base + self.str_stats + self.str_eqp
        self.dex_max = self.dex_base + self.dex_stats + self.dex_eqp
        self.int_max = self.int_base + self.int_stats + self.int_eqp
        self.vit_max = self.vit_base + self.vit_stats + self.vit_eqp
        self.luck_max = self.luck_base + self.luck_stats + self.luck_eqp
        self.hp_stats = self.vit_max * self.hp_vit_koef
        self.hp_lvl = self.lvl * self.hp_lvl_koef
        self.hp_max = self.hp_base + self.hp_stats + self.hp_lvl + self.hp_eqp

    # AKTUALIZACE DMG:
    
        weapon = self.items.filter(category='weapon', item_status='equipped').first() # Předpokládáme, že hráč může mít vybavenou pouze jednu zbraň
        armor_eqp = self.items.filter(category='armor', item_status='equipped').first() # Předpokládáme, že hráč může mít vybavenou pouze jednu zbroj   
        
        if weapon:
            print("ZBRAŇ: ANO")
            if weapon.dmg_type == 'heavy':
                dmg_atr = 'str'
            elif weapon.dmg_type == 'light':
                dmg_atr = 'dex'
            elif weapon.dmg_type == 'magic':
                dmg_atr = 'int'
        else:
            print("ZBRAŇ: NE")
            dmg_atr = 'none'
            
        if armor_eqp:
            print("ARMOR: ANO")
        else:
            print("ARMOR: NE")
        
        self.dmg_atr = dmg_atr
        self.dmg_atr_value = getattr(self, f"{self.dmg_atr}_max") if weapon and weapon.dmg_type in ['heavy', 'light', 'magic'] else 1
        
        self.dmg_base = round(self.dmg_atr_value + weapon.dmg_avg if weapon else self.lvl)
        self.dmg_min = round((self.dmg_base * weapon.dmg_min) if weapon else self.dmg_base * 0.8)  
        self.dmg_max = round((self.dmg_base * weapon.dmg_max) if weapon else self.dmg_base * 1.2)  
        self.dmg_avg = round((self.dmg_min + self.dmg_max) // 2)
        print(f"DEBUG: DMG_base: {self.dmg_base}, DMG_min: {self.dmg_min}, DMG_max: {self.dmg_max}, DMG_avg: {self.dmg_avg} for {self.username}")
        
    # AKTUALIZACE CRITICU
    
        self.crit_chance = (self.luck_stats // self.lvl) if self.luck_stats > 0 else 0
        if self.crit_chance > 50:
            self.crit_chance = 50
        
    # AKTUALIZACE ODOLNOSTÍ
    
        self.str_resist = round((self.str_max // self.lvl), 2) if self.str_max > 0 else 0
        if self.str_resist > 50:
            self.str_resist = 50
        self.dex_resist = round((self.dex_max // self.lvl), 2) if self.dex_max > 0 else 0
        if self.dex_resist > 50:
            self.dex_resist = 50
        self.int_resist = round((self.int_max // self.lvl), 2) if self.int_max > 0 else 0
        if self.int_resist > 50:
            self.int_resist = 50
            
            
    # AKTUALIZACE ARMORU
        armor_eqp = self.items.filter(category='armor', item_status='equipped').first() or None
        self.armor = armor_eqp.armor if armor_eqp else 0
        
        print("SAVE DOKONČEN")
        super().save(*args, **kwargs)
        
        
    def atr_up(self, updates):
        print(f"DEBUG: Starting attribute update for {self.username} with updates: {updates}")   
        total_spent = 0
        
        for atr_name, amount in updates.items():
            if amount <= 0:
                continue
                
            atr_name = atr_name.lower()
            
            if atr_name == 'str':
                for i in range(amount):
                    self.str_stats += 1
            elif atr_name == 'dex':
                for i in range(amount):
                    self.dex_stats += 1
            elif atr_name == 'int':
                for i in range(amount):
                    self.int_stats += 1
            elif atr_name == 'luck':
                for i in range(amount):
                    self.luck_stats += 1
            elif atr_name == 'vit':
                for _ in range(amount):
                    self.vit_stats += 1
            else:
                continue
                
            total_spent += amount
        
        if total_spent > 0:
                self.atr_points -= total_spent
                self.save()

class Player_Items_EQP_ABLE(models.Model):
    CATEGORY_CHOICES = [
        ('weapon', 'Weapon'),
        ('armor', 'Armor'),
        ('material', 'Material'),
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
    item_base_id = models.IntegerField(blank=True, null=True) # odkaz na základní item pro případ upgradu a generování, může být null pro unikátní předměty vytvořené jen pro hráče
    item_id = models.AutoField(primary_key=True, unique=True) # unikátní ID pro každý konkrétní item, které se nikdy nemění, i když se mění item_base_id při upgradu
    item_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='none')
    
    amount = models.IntegerField(default=1, validators=[MinValueValidator(1)]) # pro stackovatelné předměty, jako jsou materiály, může být více kusů stejného itemu, pro ne-stackovatelné předměty bude vždy 1

    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True) 
    category = models.CharField(max_length=50, null=True, blank=True)
    
    dmg_type = models.CharField(null=True, blank=True, max_length=50, choices=DMG_TYPE_CHOICES)
    lvl_req = models.IntegerField(null=True, blank=True)
    rarity = models.CharField(null=True, blank=True, max_length=20, choices=RARITY_CHOICES)
    price_ks = models.FloatField(null=True, blank=True, validators=[MinValueValidator(1)])
    price_all = models.FloatField(null=True, blank=True, validators=[MinValueValidator(1)])
    
    dmg_min = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    dmg_max = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    dmg_avg = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    
    armor = models.IntegerField(null=True, blank=True)
   
    item_bonus = models.JSONField(null=True, blank=True, default=dict)  # Ukládá bonusy z předmětu jako JSON


    def __str__(self):
        return f"{self.name} (ID: {self.item_id}) - {self.category} - {self.rarity} - Status: {self.item_status}"

class Player_Item_Material(models.Model):
    CATEGORY_CHOICES = [
        ('weapon', 'Weapon'),
        ('armor', 'Armor'),
        ('material', 'Material'),
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
    
    player = models.ForeignKey(Player_info, on_delete=models.CASCADE, related_name='materials')
    item_base_id = models.IntegerField(blank=True, null=True) # odkaz na základní item pro případ upgradu a generování, může být null pro unikátní předměty vytvořené jen pro hráče
    item_id = item_id = models.AutoField(primary_key=True, unique=True)
    item_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='none')
    amount = models.IntegerField(default=1, validators=[MinValueValidator(1)]) # pro stackovatelné předměty, jako jsou materiály, může být více kusů stejného itemu, pro ne-stackovatelné předměty bude vždy 1

    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)

    lvl_req = models.IntegerField(null=True, blank=True)
    rarity = models.CharField(null=True, blank=True, max_length=20, choices=RARITY_CHOICES)
    price_ks = models.FloatField(null=True, blank=True, validators=[MinValueValidator(1)])
    price_all = models.FloatField(null=True, blank=True, validators=[MinValueValidator(1)])
    
    stack_able = models.BooleanField(default=True) # určuje, zda lze předmět stakovat (např. materiály) nebo ne (např. zbraně a zbroje)
    max_stack = models.IntegerField(default=50, validators=[MinValueValidator(1)], blank=True, null=True) # maximální počet kusů stejného předmětu v jednom stacku, relevantní pouze pro stackovatelné předměty

    def __str__(self):
        return f"{self.name} (ID: {self.item_base_id}) - {self.rarity} - Amount: {self.amount}"
    