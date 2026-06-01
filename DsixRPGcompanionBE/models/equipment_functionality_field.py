from django.db import models
from ..models.equipment_functionality_type import EquipmentFunctionalityType


class EquipmentFunctionalityField(models.Model):
    """Fields that describe a functionality type"""
    functionality_type = models.ForeignKey(EquipmentFunctionalityType, on_delete=models.CASCADE, related_name='fields')
    field_name = models.CharField(max_length=100)
    field_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['functionality_type', 'field_order']
    
    def __str__(self):
        return f"{self.functionality_type.name}.{self.field_name}"