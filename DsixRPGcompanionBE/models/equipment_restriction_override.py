from django.db import models
from .character import Character
from .equipment import Equipment


class EquipmentRestrictionOverride(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='equipment_overrides')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='character_overrides')
    can_equip = models.BooleanField(default=True)
    reason = models.CharField(max_length=269, null=True, blank=True)
    granted_by = models.CharField(max_length=113, null=True, blank=True)
    
    class Meta:
        unique_together = ['character', 'equipment']
    
    def __str__(self):
        return f"Override: {self.character.name} can {'equip' if self.can_equip else 'NOT equip'} {self.equipment.name}" 