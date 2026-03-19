from django.db import models

class Player_info(models.Model):
    username = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.username.username