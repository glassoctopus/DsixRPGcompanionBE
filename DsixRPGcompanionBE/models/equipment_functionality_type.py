from django.db import models

class EquipmentFunctionalityType(models.Model):
    """weapon functionality type, i.e. shoots projectiles, provides armor, communcator"""
    name = models.CharField(max_length=113)
    description = models.CharField(max_length=666)
    
    def __str__(self):
        return self.name
    