from django.db import models
from ..models.equipment_functionality import EquipmentFunctionality
from ..models.equipment_functionality_field import EquipmentFunctionalityField


class EquipmentFunctionalityCode(models.Model):
    """Each atomic value for a functionality"""
    equipment_functionality = models.ForeignKey(EquipmentFunctionality, on_delete=models.CASCADE, related_name='values')
    field = models.ForeignKey(EquipmentFunctionalityField, on_delete=models.CASCADE)
    value = models.CharField(max_length=500)
    
    class Meta:
        unique_together = ['equipment_functionality_field', 'field']
    
    def __str__(self):
        return f"{self.field.field_name}: {self.value}"