from django.db import models
from .character import Character
from .species import Species

class CharacterSpecies(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character_species')
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='species_characters')

    def __str__(self):
        return f"{self.character.model_name} - {self.species.species_name}"
    
    class Meta:
        verbose_name = "Character Species"