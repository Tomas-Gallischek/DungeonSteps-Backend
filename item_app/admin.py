from django.contrib import admin
from .models import Item_default, All_Items_Bonus, Item_Armor_Submodel, Item_Weapon_Submodel, Item_Material_Submodel, Item_Helmet_Submodel, Item_Boots_Submodel, Item_Amulet_Submodel, Item_Ring_Submodel, Item_Talisman_Submodel, Item_Pet_Submodel, ItemUpgrade, UpgradeMaterial

admin.site.register(Item_default)
admin.site.register(All_Items_Bonus)
admin.site.register(Item_Armor_Submodel)
admin.site.register(Item_Weapon_Submodel)
admin.site.register(Item_Material_Submodel)
admin.site.register(Item_Helmet_Submodel)
admin.site.register(Item_Boots_Submodel)
admin.site.register(Item_Amulet_Submodel)
admin.site.register(Item_Ring_Submodel)
admin.site.register(Item_Talisman_Submodel)
admin.site.register(Item_Pet_Submodel)

class UpgradeMaterialInline(admin.TabularInline):
    model = UpgradeMaterial
    extra = 0
    verbose_name = "Potřebný materiál"
    verbose_name_plural = "Potřebné materiály"

class ItemUpgradeInline(admin.TabularInline):
    model = ItemUpgrade
    extra = 0
    show_change_link = True # TOTO JE KLÍČOVÉ: Přidá odkaz "Změnit", který tě hodí do detailu upgradu k materiálům
    fields = ('lvl', 'gold_cost')
    verbose_name = "Stupeň vylepšení"
    verbose_name_plural = "Stupně vylepšení"

@admin.register(ItemUpgrade)
class ItemUpgradeAdmin(admin.ModelAdmin):
    list_display = ('item', 'lvl', 'gold_cost')
    list_filter = ('item', 'lvl')
    inlines = [UpgradeMaterialInline]
    search_fields = ('item__name',)
    actions = ['resave_items', 'duplicate_items']
    
    @admin.action(description='PŘEPOČET CENY')
    def resave_items(modeladmin, request, queryset):
        # queryset obsahuje položky, které jsi v administraci zaškrtl
        for obj in queryset:
            obj.save() # Zde se zavolá tvoje upravená metoda save()
        
        # Zobrazíme zelenou hlášku o úspěchu
        modeladmin.message_user(request, f"Úspěšně přepočítáno {queryset.count()} záznamů.")
    

    @admin.action(description="AUTO DOPLNĚNÍ UPGRADE (Doplň hodnoty v admin.py !!!!)")
    def duplicate_items(self, request, queryset):
    
    # NASTAVENÍ HODNOT:
        amount_to_create = 9  # Vytvoříme 9 kopií, abychom měli celkem 10 levelů
        created_count = 0
        max_material_kind = 4
    
    # PO KOLIKA SE BUDOU MATERIÁLY ZVYŠOVAT
        mat_1_koef = 1
        mat_2_koef = 2
        mat_3_koef = 5
        mat_4_koef = 0
        
    # LVL, kdy se přidá nový materiál:
    
    # Pokud chceš méně materiálů, zadej třeba lvl 100 a kod se neprovede
        mat_1_lvl = 1 
        mat_2_lvl = 1
        mat_3_lvl = 5 # ZADAT O 1 MÍN NEŽ CHCEŠ !
        mat_4_lvl = 100 # ZADAT O 1 MÍN NEŽ CHCEŠ !
        
        
        
        # Obrana proti tomu, když by uživatel vybral víc než 1 záznam naráz
        if queryset.count() > 1:
            self.message_user(request, "Tato akce funguje pouze pokud vyberete přesně JEDEN počáteční záznam.", level="ERROR")
            return

        # Získáme ten jeden vybraný záznam (nejčastěji Lvl 1)
        original_obj = queryset.first()
        
        # Zapamatujeme si původní materiály
        original_materials = list(original_obj.materials.all())
        


        for i in range(1, amount_to_create + 1):
            # 1. Zkopírujeme základní objekt
            new_upgrade = ItemUpgrade.objects.get(pk=original_obj.pk)
            new_upgrade.pk = None  # Django pochopí, že má vytvořit nový záznam
            new_upgrade.lvl = original_obj.lvl + i
            
            try:
                new_upgrade.save()
                created_count += 1
                ciklus = 0
                for mat in original_materials: # KDYŽ NASTAVÍM HNED U PRVNÍHO ZÁZNAMU VŠECHNY 4 MATERIÁLY, PROVEDOU SE 4 CYKLY
                    ciklus += 1
                    if ciklus > max_material_kind:
                        break
                    
                # 1. MATERIAL
                    if ciklus == 1: 
                        if i >= mat_1_lvl:
                            amount = mat_1_koef * (i - (mat_1_lvl - 1))
                # 2. MATERIAL
                    elif ciklus == 2: 
                        if i >= mat_2_lvl:
                            amount = mat_2_koef * (i - (mat_2_lvl - 1))
                # 3. MATERIAL     
                    elif ciklus == 3: 
                        if i >= mat_3_lvl:
                            amount = mat_3_koef * (i - (mat_3_lvl - 1))
                        else:
                            amount = 0
                # 4. MATERIAL     
                    elif ciklus == 4: 
                        if i >= mat_4_lvl:
                            amount = mat_4_koef * (i - (mat_4_lvl - 1))
                        else:
                            amount = 0

                    new_material = UpgradeMaterial(
                        upgrade=new_upgrade, # ITEM, NA KTERÝ POŽADAVEK NAPOJUJEME
                        material=mat.material, # POTŘEBNÉ MATERIÁLY Z PŮVODNÍHO UPGRADU
                        amount=mat.amount + amount # MNOŽSTVÍ
                    )
                    if new_material.amount > 0: # ULOŽÍME POUZE MATERIÁLY, KTERÉ MAJÍ KLADNÉ MNOŽSTVÍ
                        new_material.save()
                    else:
                        pass
                    
            except Exception as e:
                # Zachytí chybu (např. kdyby level už existoval kvůli unique_together)
                self.message_user(request, f"Chyba při vytváření Lvl {new_upgrade.lvl}: {e}", level="WARNING")
                break # Zastavíme cyklus, ať se nedělají další nesmysly

        if created_count > 0:
            self.message_user(request, f"Úspěšně vytvořeno {created_count} kopií i s materiály.")
        else:
            self.message_user(request, "Žádné nové kopie nebyly vytvořeny.", level="WARNING")

# ... (registrace adminu atd.)