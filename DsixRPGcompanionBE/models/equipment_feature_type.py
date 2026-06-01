from django.db import models


class EquipmentFeatureType(models.Model):
    """Types of features that equipment can have (passive attributes)"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name