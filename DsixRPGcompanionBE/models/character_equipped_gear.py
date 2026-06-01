from django.db import models
from .character import Character
from .character_equipment import CharacterEquipment

class CharacterEquippedGear(models.Model):
    GEAR_SLOTS = [
        ('head', 'Head'),
        ('eyes', 'Eyes'),
        ('ears', 'Ears'),
        ('back', 'Back'),
        ('chest', 'Chest'),
        ('wrist', 'Wrist'),
        ('belt', 'Belt'),        
        ('leg', 'Leg'),
        ('foot', 'Foot'),
    ]
    
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='equipped_gear')
    character_equipment = models.ForeignKey(CharacterEquipment, on_delete=models.CASCADE, related_name='equipped_as_gear')
    slot = models.CharField(max_length=5, choices=GEAR_SLOTS)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Equipped Gear"
        verbose_name_plural = "Equipped Gear"
        unique_together = ['character', 'slot']
    
    def __str__(self):
        return f"{self.character.name}'s {self.character_equipment.equipment.name} ({self.slot})"
    
    def save(self, *args, **kwargs):
        self.character_equipment.status = 'equipped'
        self.character_equipment.save()
        super().save(*args, **kwargs)
