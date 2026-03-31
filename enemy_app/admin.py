from django.contrib import admin
from .models import Enemy, loot, loot_gold

admin.site.register(Enemy)
admin.site.register(loot)
admin.site.register(loot_gold)

# Register your models here.
