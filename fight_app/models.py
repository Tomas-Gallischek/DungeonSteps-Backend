from django.db import models
from profile_app.models import Player_info


class fight_log(models.Model):
    player = models.ForeignKey(Player_info, on_delete=models.CASCADE)
    all_enemies_defeded = models.JSONField(default=list)
    defeinitive_winner = models.CharField(max_length=100)
    
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    time_duration_seconds = models.FloatField()  # Doba trvání souboje v sekundách
    
    turn_logs = models.JSONField(default=list)  # List of dictionaries with turn details