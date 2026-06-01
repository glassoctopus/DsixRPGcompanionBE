from django.db import models
from django.core.validators import MinValueValidator
from .character import Character
from .archetype import Archetype
from .species import Species
from .skill import Skill

class Equipment(models.Model):
    # Universal fields
    name = models.CharField(max_length=269)
    category = models.CharField(max_length=269)
    sub_category = models.CharField(max_length=269, null=True, blank=True)
    model = models.CharField(max_length=269, null=True, blank=True)
    type = models.CharField(max_length=113, null=True, blank=True)
    scale = models.CharField(max_length=113, null=True, blank=True)  # Character, Speeder, Walker, Starfighter, Capital
    cost = models.IntegerField(default=0)
    description = models.CharField(max_length=1369, null=True, blank=True)
    availability = models.CharField(max_length=26, null=True, blank=True)  # Restricted, Licensed, Illegal, Common
    skill = models.CharField(max_length=113, null=True, blank=True)
    use_notes = models.CharField(max_length=3666, null=True, blank=True)
    source = models.CharField(max_length=1369, null=True, blank=True)
    
    # These are ultimatly at the GM discreation, leaving them in case a GM prefers to track
    weight_kg = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    encumbrance_value = models.IntegerField(default=0)
    
    is_weapon = models.BooleanField(default=False)
    is_armor = models.BooleanField(default=False)
    is_gear = models.BooleanField(default=False)
    is_tool = models.BooleanField(default=False)
    is_computer = models.BooleanField(default=False)
    is_communication = models.BooleanField(default=False)
    is_scanner = models.BooleanField(default=False)
    is_survival = models.BooleanField(default=False)
    is_medical = models.BooleanField(default=False)
    is_droid_accessory = models.BooleanField(default=False)
    is_cybernetic = models.BooleanField(default=False)
    is_explosive_device = models.BooleanField(default=False)
    is_restraint = models.BooleanField(default=False)
    is_mobility = models.BooleanField(default=False)
    
    required_archetypes = models.ManyToManyField(Archetype, blank=True, related_name='restricted_equipment')
    prohibited_archetypes = models.ManyToManyField(Archetype, blank=True, related_name='prohibited_equipment')
    required_species = models.ManyToManyField(Species, blank=True, related_name='restricted_equipment')
    prohibited_species = models.ManyToManyField(Species, blank=True, related_name='prohibited_equipment')
    required_skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name='required_for_equipment')
    required_skill_rank = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"

