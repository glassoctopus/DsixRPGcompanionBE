from django.db import models
from ..models.equipment import Equipment
from ..models.equipment_feature_type import EquipmentFeatureType


class EquipmentFeature(models.Model):
    """Each distinct feature an equipment item has (passive attributes)"""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='features')
    feature_type = models.ForeignKey(EquipmentFeatureType, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True)
    
    def __str__(self):
        return f"{self.equipment.name}: {self.feature_type.name}"