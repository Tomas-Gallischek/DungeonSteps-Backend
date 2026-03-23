from django.db import models
from profile_app.models import Player_info
from enemy_app.models import Enemy


class fight_log(models.Model):
    player = models.ForeignKey(Player_info, on_delete=models.CASCADE)
    enemy = models.ForeignKey(Enemy, on_delete=models.CASCADE)
    
    winner = models.CharField(max_length=100)
    
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    
    turn_logs = models.JSONField(default=list)  # List of dictionaries with turn details