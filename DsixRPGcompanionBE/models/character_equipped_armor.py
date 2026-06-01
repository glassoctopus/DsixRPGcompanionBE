from django.db import models
from .character import Character
from .character_equipment import CharacterEquipment

class CharacterEquippedArmor(models.Model):
    """Currently equipped armor of character"""
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='equipped_armor')
    character_equipment = models.ForeignKey(CharacterEquipment, on_delete=models.CASCADE, related_name='equipped_as_armor')
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.character.name}'s {self.character_equipment.equipment.name}"
    
    def save(self, *args, **kwargs):
        self.character_equipment.status = 'equipped'
        self.character_equipment.save()
        super().save(*args, **kwargs)