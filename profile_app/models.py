from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone



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
    
    PLAYER_TYPER_CHOICES = [
        ('player', 'Player'),
        ('bot', 'Bot'),
        ('test', 'Test'),
    ]
    
# ZÁKLADNÍ INFORMACE
    username = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default=None, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=None, null=True, blank=True)
    lvl = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    xp = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    xp_next_lvl = models.IntegerField(default=8000, validators=[MinValueValidator(1)])
    gold = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    dungeon_tokens = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
# STAVY
    active_status = models.BooleanField(default=False, help_text="Aktivní/Odhlášený")
    ban_status = models.BooleanField(default=False, help_text="BAN: Ano/Ne.")
    player_type = models.CharField(max_length=10, choices=PLAYER_TYPER_CHOICES, default='player')
    last_login = models.DateTimeField(null=True, blank=True)
    registration_date = models.DateTimeField(blank=True, null=True)
    
    busy_until = models.DateTimeField(null=True, blank=True, help_text="Čas, dokdy je hráč na výpravě nebo v s  ouboji.")

    @property
    def is_busy(self):
        """Vrátí True, pokud je hráč aktuálně na výpravě (čas busy_until ještě nevypršel)."""
        if self.busy_until and self.busy_until > timezone.now():
            return True
        return False

# OBRÁZKY
    avatar_img_ozn = models.CharField(default='avatar_default', max_length=100, null=True, blank=True)
    player_bg_img = models.CharField(default='background_default', max_length=100, null=True, blank=True)

# POINTS
    atr_points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    skill_points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    energy_points = models.IntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])

# KROKY
    steps = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    steps_today = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(30000)])
    
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

    mana_base = models.IntegerField(default=0, blank=True)
    mana_stats = models.IntegerField(default=0, blank=True)
    mana_lvl = models.IntegerField(default=0, blank=True)
    mana_eqp = models.IntegerField(default=0, blank=True)
    mana_max = models.IntegerField(default=0, blank=True)
    mana_lvl_koef = models.IntegerField(("Mana Level Coefficient"), default=5, blank=True)  # Koeficient pro výpočet many z úrovně


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
    
    prec_base = models.IntegerField(default=1, blank=True)
    prec_stats = models.IntegerField(default=0, blank=True)
    prec_eqp = models.IntegerField(default=0, blank=True)
    prec_max = models.IntegerField(default=1, blank=True)
    
# BOJ
    dmg_base = models.IntegerField(default=1, blank=True) # <-- Základní poškození, které se bude upravovat podle atributů a vybavení
    dmg_avg = models.IntegerField(default=2, blank=True)
    dmg_min = models.IntegerField(default=1, blank=True)
    dmg_max = models.IntegerField(default=3, blank=True)
    prum_skoda = models.FloatField(default=0, blank=True) # <-- Průměrná škoda, která se bude počítat z dmg_avg a bonusů z vybavení a petů
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
        print(f"DEBUG: Spouštím save() pro {self.username} ...")
    # PŘI REGISTRACI JE NUTNO PRVNBĚ VŠECHNO ULOŽIT A AŽ PAK SPUSTIT METODU SAVE() ZNOVA
        if self.gender is None or self.role is None:
            super().save(*args, **kwargs)
            return
        
        
# NAČTENÍ VYBAVENÍ
        weapon_eqp = self.items.filter(category='weapon', item_status='equipped').first() # Předpokládáme, že hráč může mít vybavenou pouze jednu zbraň
        armor_eqp = self.items.filter(category='armor', item_status='equipped').first() # Předpokládáme, že hráč může mít vybavenou pouze jednu zbroj
        helmet_eqp = self.items.filter(category='helmet', item_status='equipped').first() # Předpokládáme, že hráč může mít vybavenou pouze jednu helmu
        boots_eqp = self.items.filter(category='boots', item_status='equipped').first() # Předpokládáme, že hráč může mít vybavené pouze jedny boty
        amulet_eqp = self.items.filter(category='amulet', item_status='equipped').first() # Předpokládáme, že hráč může mít vybavený pouze jeden amulet
        ring_eqp = self.items.filter(category='ring', item_status='equipped').first() # Předpokládáme, že hráč může mít vybavený pouze jeden prsten
        # TALISMANY není třeba načítat protože v kodu nemají vyuřití, protože jejich bonusy se generují až na úrovni hráče a jsou uloženy přímo v itemu, takže se načítají automaticky s vybavením
        pet_eqp = self.items.filter(category='pet', item_status='equipped').first() # Předpokládáme, že hráč může mít vybaveného pouze jednoho peta
              
              
            
# NAČTENÍ VŠECH BONUSŮ Z VYBAVENÍ
        equipped_items = list(self.items.filter(item_status='equipped'))

        self.str_eqp = sum(item.item_bonusy.get('str', 0) for item in equipped_items)
        self.dex_eqp = sum(item.item_bonusy.get('dex', 0) for item in equipped_items)
        self.int_eqp = sum(item.item_bonusy.get('int', 0) for item in equipped_items)
        self.vit_eqp = sum(item.item_bonusy.get('vit', 0) for item in equipped_items)
        self.luck_eqp = sum(item.item_bonusy.get('luck', 0) for item in equipped_items)
        self.prec_eqp = sum(item.item_bonusy.get('prec', 0) for item in equipped_items)
                                        
# PETI        
        if pet_eqp:
            pet_lvl = pet_eqp.pet_lvl if pet_eqp.pet_lvl else 1
            pet_armor_bonus = (pet_eqp.pet_armor_bonus if pet_eqp.pet_armor_bonus else 0) * pet_lvl
            pet_dmg_bonus = (pet_eqp.pet_dmg_bonus if pet_eqp.pet_dmg_bonus else 0) * pet_lvl
            pet_hp_bonus = (pet_eqp.pet_hp_bonus if pet_eqp.pet_hp_bonus else 0) * pet_lvl
            pet_prum_skoda_bonus = (pet_eqp.pet_prum_skoda_bonus if pet_eqp.pet_prum_skoda_bonus else 0) * pet_lvl
        else:
            pet_armor_bonus = 0
            pet_dmg_bonus = 0
            pet_hp_bonus = 0
            pet_prum_skoda_bonus = 0
                                       
# AMULETY A PRSTENY - PŘIDÁNÍ BONUSŮ Z AMULETU A PRSTENŮ

        if amulet_eqp:
            self.str_eqp += round(amulet_eqp.all_atr_bonus_amulet * self.str_base)
            self.dex_eqp += round(amulet_eqp.all_atr_bonus_amulet * self.dex_base)
            self.int_eqp += round(amulet_eqp.all_atr_bonus_amulet * self.int_base)
            self.vit_eqp += round(amulet_eqp.all_atr_bonus_amulet * self.vit_base)
            self.luck_eqp += round(amulet_eqp.all_atr_bonus_amulet * self.luck_base)
        else:
            self.str_eqp += 0
            self.dex_eqp += 0
            self.int_eqp += 0
            self.vit_eqp += 0
            self.luck_eqp += 0
        
        if ring_eqp:
            self.str_eqp += round(ring_eqp.all_atr_bonus_ring * self.str_base)
            self.dex_eqp += round(ring_eqp.all_atr_bonus_ring * self.dex_base)
            self.int_eqp += round(ring_eqp.all_atr_bonus_ring * self.int_base)
            self.vit_eqp += round(ring_eqp.all_atr_bonus_ring * self.vit_base)
            self.luck_eqp += round(ring_eqp.all_atr_bonus_ring * self.luck_base) 
        else:
                self.str_eqp += 0
                self.dex_eqp += 0
                self.int_eqp += 0
                self.vit_eqp += 0
                self.luck_eqp += 0
# ZBRANĚ
        
        if weapon_eqp:
            if weapon_eqp.dmg_type == 'heavy':
                dmg_atr = 'str'
            elif weapon_eqp.dmg_type == 'light':
                dmg_atr = 'dex'
            elif weapon_eqp.dmg_type == 'magic':
                dmg_atr = 'int'
        else:
            dmg_atr = 'none'
        
        self.prum_skoda = 1 + pet_prum_skoda_bonus # PŘIDAT ČASEM Z BONUSŮ
        
        self.dmg_atr = dmg_atr
        self.dmg_atr_value = getattr(self, f"{self.dmg_atr}_max") if weapon_eqp and weapon_eqp.dmg_type in ['heavy', 'light', 'magic'] else 1
        
        self.dmg_base = round((self.dmg_atr_value + weapon_eqp.dmg_avg + pet_dmg_bonus) * self.prum_skoda if weapon_eqp else self.lvl + self.dmg_atr_value)
        self.dmg_min = round((self.dmg_base + weapon_eqp.dmg_min) if weapon_eqp else self.dmg_base * 0.8)  
        self.dmg_max = round((self.dmg_base + weapon_eqp.dmg_max) if weapon_eqp else self.dmg_base * 1.2)  
        self.dmg_avg = round((self.dmg_min + self.dmg_max) // 2)
        
# RYCHLOST ÚTOKU
    # Základ je ze zbraně
        base_attack_speed = weapon_eqp.attack_speed_weapon if weapon_eqp and weapon_eqp.attack_speed_weapon else 1
    # Ostatní itemy jen přidávají/ubírají procenta
    
        if armor_eqp and armor_eqp.attack_speed_armor:
            armor_attack_speed_bonus = base_attack_speed * armor_eqp.attack_speed_armor
        else:
            armor_attack_speed_bonus = 0         
        if helmet_eqp and helmet_eqp.attack_speed_helmet:
            helmet_attack_speed_bonus = base_attack_speed * helmet_eqp.attack_speed_helmet
        else:
            helmet_attack_speed_bonus = 0
        if boots_eqp and boots_eqp.attack_speed_boots:
            boots_attack_speed_bonus = base_attack_speed * boots_eqp.attack_speed_boots
        else:
            boots_attack_speed_bonus = 0

        print(f"DEBUG: base_attack_speed={base_attack_speed}, armor_bonus={armor_attack_speed_bonus}, helmet_bonus={helmet_attack_speed_bonus}, boots_bonus={boots_attack_speed_bonus}")
        self.attack_speed = base_attack_speed + armor_attack_speed_bonus + helmet_attack_speed_bonus + boots_attack_speed_bonus
        
# AKTUALIZACE ARMORU
        brneni_armor = armor_eqp.armor if armor_eqp else 0
        helma_armor = helmet_eqp.armor if helmet_eqp else 0
        boty_armor = boots_eqp.armor if boots_eqp else 0
        self.armor = brneni_armor + helma_armor + boty_armor + pet_armor_bonus
        
# AKTUALIZACE HP
        self.hp_eqp = armor_eqp.plus_hp if armor_eqp and armor_eqp.plus_hp else 0
        self.hp_eqp += pet_hp_bonus
        
    # AKTUALIZACE ATRIBUTŮ (Provádět až po načtení všech bonusů z vybavení, protože některé bonusy z amuletů a prstenů závisí na základních a statistických atributech)
        self.str_max = self.str_base + self.str_stats + self.str_eqp
        self.dex_max = self.dex_base + self.dex_stats + self.dex_eqp
        self.int_max = self.int_base + self.int_stats + self.int_eqp
        self.vit_max = self.vit_base + self.vit_stats + self.vit_eqp
        self.luck_max = self.luck_base + self.luck_stats + self.luck_eqp
        self.hp_stats = self.vit_max * self.hp_vit_koef
        self.hp_lvl = self.lvl * self.hp_lvl_koef
        self.hp_max = self.hp_base + self.hp_stats + self.hp_lvl + self.hp_eqp

    # AKTUALIZACE CRITICU (Závisí na atr, proto je to tady)
    
        self.crit_chance = (self.luck_max // self.lvl) if self.luck_max > 0 else 0
        if self.crit_chance > 50:
            self.crit_chance = 50
        
        
    # AKTUALIZACE ODOLNOSTÍ (Závisí na atr, proto je to tady)
    
        self.str_resist = round((self.str_max // self.lvl), 2) if self.str_max > 0 else 0
        if self.str_resist > 50:
            self.str_resist = 50
        self.dex_resist = round((self.dex_max // self.lvl), 2) if self.dex_max > 0 else 0
        if self.dex_resist > 50:
            self.dex_resist = 50
        self.int_resist = round((self.int_max // self.lvl), 2) if self.int_max > 0 else 0
        if self.int_resist > 50:
            self.int_resist = 50
            
        super().save(*args, **kwargs)
            
            
    def atr_up(self, updates):
        print(f"DEBUG: Starting attribute update for {self.username} with updates: {updates}")   
        total_spent = 0
        
        for atr_name, amount in updates.items():
            if amount <= 0:
                continue
                
            atr_name = atr_name.lower()
            
            if atr_name == 'str':
                self.str_stats += amount
            elif atr_name == 'dex':
                self.dex_stats += amount
            elif atr_name == 'int':
                self.int_stats += amount
            elif atr_name == 'luck':
                self.luck_stats += amount
            elif atr_name == 'vit':
                self.vit_stats += amount
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
    
    DMG_TYPE_CHOICES = [
        ('heavy', 'Heavy'),
        ('light', 'Light'),
        ('magic', 'Magic'),
        ('none', 'None'),
    ]
    
    STATUS_CHOICES = [
        ('equipped', 'Equipped'),
        ('inventory', 'Inventory'),
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
    
# OBECNÉ
    player = models.ForeignKey(Player_info, on_delete=models.CASCADE, related_name='items')
    item_id = models.AutoField(primary_key=True, unique=True) # unikátní ID pro každý konkrétní item
    item_base_id = models.IntegerField(blank=True, null=True) # odkaz na základní item pro případ upgradu a generování, může být null pro unikátní předměty vytvořené jen pro hráče
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True) 
    item_img_ozn = models.CharField(default='item_default', max_length=100, null=True, blank=True) # odkaz na obrázek itemu, může být null pro unikátní předměty vytvořené jen pro hráče
    item_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inventory')
    stack_able = models.BooleanField(default=False)
    item_lvl = models.IntegerField(default=0)
    
    amount = models.IntegerField(default=1)
    category = models.CharField(max_length=50, null=True, blank=True, choices=CATEGORY_CHOICES, default=None)
    lvl_req = models.IntegerField(null=True, blank=True, default=1)
    shop_max_lvl_drop = models.IntegerField(null=True, blank=True, default=99)
    
    rarity = models.CharField(null=True, blank=True, max_length=20, choices=RARITY_CHOICES)
    item_bonusy = models.JSONField(null=True, blank=True, default=dict)  # Ukládá bonusy z předmětu jako JSON
    price_ks = models.FloatField(null=True, blank=True, default=0.1)
    price_all = models.FloatField(null=True, blank=True, default=0.1)
    
    armor = models.IntegerField(null=True, blank=True)
    dmg_type = models.CharField(null=True, blank=True, max_length=50, choices=DMG_TYPE_CHOICES)

# POUZE ZBRANĚ
    dmg_min = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    dmg_max = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    dmg_avg = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    
# ATTACK SPEED - U ZBRANÍ, BRNĚNÍ, HELMŮ A BOT
    attack_speed_weapon=models.FloatField(null=True, blank=True, default=None)
    attack_speed_armor=models.FloatField(null=True, blank=True, default=None)
    attack_speed_helmet=models.FloatField(null=True, blank=True, default=None)
    attack_speed_boots=models.FloatField(null=True, blank=True, default=None)
    
# POUZE BRNĚNÍ
    plus_hp = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)], default=0)

# POUZE AMULETY
    all_atr_bonus_amulet = models.FloatField(null=True, blank=True, default=0)

# POUZE PRSTENY
    all_atr_bonus_ring = models.FloatField(null=True, blank=True, default=0)
    
# POUZE PRO TALISMANY
    talisman_bonus_name = models.CharField(max_length=255, null=True, blank=True, default=None)
    talisman_bonus_type = models.CharField(max_length=50, null=True, blank=True, default=None)
    talisman_bonus_value = models.FloatField(null=True, blank=True, default=0)

# POUZE PRO PETY
    pet_lvl = models.IntegerField(null=True, blank=True, default=None)
    pet_armor_bonus = models.FloatField(null=True, blank=True, default=None)
    pet_dmg_bonus = models.FloatField(null=True, blank=True, default=None)
    pet_hp_bonus = models.FloatField(null=True, blank=True, default=None)
    pet_prum_skoda_bonus = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name} (ID: {self.item_id}) - {self.category} - {self.rarity} - Status: {self.item_status}"

class Player_Item_Material(models.Model):
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
    
    DMG_TYPE_CHOICES = [
        ('heavy', 'Heavy'),
        ('light', 'Light'),
        ('magic', 'Magic'),
        ('none', 'None'),
    ]
    
    STATUS_CHOICES = [
        ('equipped', 'Equipped'),
        ('inventory', 'Inventory'),
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
    item_id = models.AutoField(primary_key=True, unique=True)
    item_base_id = models.IntegerField(blank=True, null=True) # odkaz na základní item pro případ upgradu a generování, může být null pro unikátní předměty vytvořené jen pro hráče
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    item_img_ozn = models.CharField(default='item_default', max_length=100, null=True, blank=True) # odkaz na obrázek itemu, může být null pro unikátní předměty vytvořené jen pro hráče
    category = models.CharField(max_length=50, null=True, blank=True, choices=CATEGORY_CHOICES, default='material')
    
    item_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inventory')
    amount = models.IntegerField(default=1)

    lvl_req = models.IntegerField(null=True, blank=True, default=1)
    rarity = models.CharField(null=True, blank=True, max_length=20, choices=RARITY_CHOICES, default='common')
    price_ks = models.FloatField(null=True, blank=True, default=0.1)
    price_all = models.FloatField(null=True, blank=True, default=0.1)
    stack_able = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (ID: {self.item_base_id}) - {self.rarity} - Amount: {self.amount}"
    