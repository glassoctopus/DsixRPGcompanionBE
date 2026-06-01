from django.db import models
from ..models.equipment_feature_type import EquipmentFeatureType


class EquipmentFeatureField(models.Model):
    """Fields that describe a feature type"""
    feature_type = models.ForeignKey(EquipmentFeatureType, on_delete=models.CASCADE, related_name='fields')
    field_name = models.CharField(max_length=100)
    field_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['feature_type', 'field_order']
    
    def __str__(self):
        return f"{self.feature_type.name}.{self.field_name}"