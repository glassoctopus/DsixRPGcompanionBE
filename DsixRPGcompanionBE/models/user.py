from django.db import models

class User():
    uid = models.CharField(max_length=113)
    bio = models.CharField(max_length=113)
    admin = models.BooleanField(default=False)
    game_master = models.BooleanField(default=False)