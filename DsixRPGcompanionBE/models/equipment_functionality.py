from django.db import models
from ..models.equipment import Equipment
from ..models.equipment_functionality_type import EquipmentFunctionalityType


class EquipmentFunctionality(models.Model):
    """Each distinct functionality an equipment item has (active effects)"""
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='functionalities')
    functionality_type = models.ForeignKey(EquipmentFunctionalityType, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True)
    
    def __str__(self):
        return f"{self.equipment.name}: {self.EquipmentFunctionalityType.name}"