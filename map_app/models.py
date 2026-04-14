from django.db import models
from enemy_app.models import Enemy  # Importuj model Enemy pro ManyToManyField

class Dungeon(models.Model):
    dungeon_base_id = models.IntegerField(("Dungeon Base ID"), unique=True)
    name = models.CharField(max_length=100, verbose_name="Název dungeonu")
    description = models.TextField(verbose_name="Popis")
    background_img = models.CharField(max_length=100, blank=True, help_text="Název obrázku ve Flutteru (např. 'bg_dark_cave')")
    icon_img = models.CharField(max_length=100, blank=True, help_text="Název ikony ve Flutteru (např. 'icon_dark_cave')")
    min_level = models.IntegerField(default=1, verbose_name="Minimální úroveň pro vstup")
    enemies = models.ManyToManyField(
        Enemy, 
        related_name='dungeons',
        blank=True,
        verbose_name="Možní nepřátelé"
    )

    def __str__(self):
        return f"{self.name} (Lvl {self.min_level}+)"
    
class Void(models.Model):
    void_base_id = models.IntegerField(("Void Base ID"), unique=True)
    name = models.CharField(max_length=100, verbose_name="Název voidu")
    description = models.TextField(verbose_name="Popis")
    background_img = models.CharField(max_length=100, help_text="Název obrázku ve Flutteru (např. 'bg_void_realm')")
    min_level = models.IntegerField(default=1, verbose_name="Minimální úroveň pro vstup")
    enemies = models.ManyToManyField(
        Enemy, 
        related_name='voids',
        blank=True,
        verbose_name="Možní nepřátelé"
    )

    def __str__(self):
        return f"{self.name} (Lvl {self.min_level}+)"
    
class WorldBoss(models.Model):
    world_boss_base_id = models.IntegerField(("World Boss Base ID"), unique=True)
    name = models.CharField(max_length=100, verbose_name="Název world bosse")
    description = models.TextField(verbose_name="Popis")
    background_img = models.CharField(max_length=100, help_text="Název obrázku ve Flutteru (např. 'bg_world_boss')")
    min_level = models.IntegerField(default=1, verbose_name="Minimální úroveň pro vstup")
    enemies = models.ManyToManyField(
        Enemy, 
        related_name='world_bosses',
        blank=True,
        verbose_name="Možní nepřátelé"
    )

    def __str__(self):
        return f"{self.name} (Lvl {self.min_level}+)"