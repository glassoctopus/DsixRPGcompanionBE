from django.db import models

class User(models.Model):
    uid = models.CharField(max_length=113)
    handle = models.CharField(max_length=113, null=True, blank=True)
    bio = models.CharField(max_length=113, null=True, blank=True)
    admin = models.BooleanField(default=False)
    game_master = models.BooleanField(default=False)
    
    def __str__(self):
        return self.uid