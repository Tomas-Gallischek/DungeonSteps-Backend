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
    extra = 1  # Kolik prázdných řádků pro materiály se má zobrazit
    verbose_name = "Potřebný materiál"
    verbose_name_plural = "Potřebné materiály"

class ItemUpgradeInline(admin.TabularInline):
    model = ItemUpgrade
    extra = 1
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
    actions = ['resave_items']
    
    @admin.action(description='Znovu uložit (přepočítat) vybrané záznamy')
    def resave_items(modeladmin, request, queryset):
        # queryset obsahuje položky, které jsi v administraci zaškrtl
        for obj in queryset:
            obj.save() # Zde se zavolá tvoje upravená metoda save()
        
        # Zobrazíme zelenou hlášku o úspěchu
        modeladmin.message_user(request, f"Úspěšně přepočítáno {queryset.count()} záznamů.")
    
    
    

    

