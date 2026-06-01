from django.db import models
from ..models.equipment_feature import EquipmentFeature
from ..models.equipment_feature_field import EquipmentFeatureField


class EquipmentFeatureCode(models.Model):
    """Each atomic value for a feature, to allow for full customization"""
    equipment_feature = models.ForeignKey(EquipmentFeature, on_delete=models.CASCADE, related_name='values')
    field = models.ForeignKey(EquipmentFeatureField, on_delete=models.CASCADE)
    value = models.CharField(max_length=500)
    
    class Meta:
        unique_together = ['equipment_feature', 'field']
    
    def __str__(self):
        return f"{self.field.field_name}: {self.value}"