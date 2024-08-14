from django.db import models

class UserGroup():
    group_name = models.CharField(max_length=69)
    game_master = models.IntegerField(default=0)
    character_id = models.IntegerField(default=0)
    private = models.BooleanField(default=False)
    is_adventure_party = models.BooleanField(default=False)