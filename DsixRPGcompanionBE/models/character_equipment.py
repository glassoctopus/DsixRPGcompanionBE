from django.db import models
from django.core.validators import MinValueValidator
from .equipment import Equipment
from .character import Character

class CharacterEquipment(models.Model):
    """Accounts for equipment owned and carried by a character"""
    EQUIPMENT_STATUS = [
        ('carried', 'Carried'),
        ('stored', 'In Storage'),
        ('equipped', 'Equipped'),
        ('dropped', 'Dropped'),
        ('destroyed', 'Destroyed'),
    ]
    EQUIPMENT_CONDITION = [
        ('new', 'New'),
        ('used', 'Used'),
        ('broken', 'Broken'),
        ('destroyed', 'Destroyed'),
    ]
    
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='inventory')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='owned_by')
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=10, choices=EQUIPMENT_STATUS, default='carried')
    condition = models.CharField(max_length=9, choices=EQUIPMENT_CONDITION, default='used')
    notes = models.CharField(max_length=666, null=True, blank=True)
    acquired_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['character', 'equipment']
        verbose_name = "Character Equipment"
        verbose_name_plural = "Character Equipment"
        
    def __str__(self):
        return f"{self.character.name} - {self.equipment.name} x{self.quantity}"
    
