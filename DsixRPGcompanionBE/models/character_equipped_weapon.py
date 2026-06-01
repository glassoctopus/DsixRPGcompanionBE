from django.db import models
from .character_equipment import CharacterEquipment
from .character import Character

class CharacterEquippedWeapon(models.Model):
    """Equipped weapons are seperate from inventory"""
    WEAPON_HAND = [
        ('primary', 'Primary Hand'),
        ('off', 'Off Hand'),
        ('two', 'Two-Handed'),
        ('holstered', 'Holstered'),
    ]
    
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='equipped_weapons')
    character_equipment = models.ForeignKey(CharacterEquipment, on_delete=models.CASCADE, related_name='equipped_as_weapon')
    hand = models.CharField(max_length=12, choices=WEAPON_HAND, default='primary')
    is_drawn = models.BooleanField(default=False)
    current_ammo = models.IntegerField(null=True, blank=True)
    current_charges = models.models.IntegerField(null=True, blank=True)
    is_loaded = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Equipped Weapon"
        verbose_name_plural = "Equipped Weapons"
        unique_together = ['character', 'hand']
        
    def __str__(self):
        return f"{self.character.name}'s {self.character_equipment.equipment.name} ({sel_f.hand})"
    
    def save(self, *args, **kwargs):
        self.character_equipment.status = 'equipped'
        self.character_equipment.save()
        super().save(*args, **kwargs)