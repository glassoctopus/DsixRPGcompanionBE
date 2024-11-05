from django.db import models

class SpeciesAbility(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='species_abilities')
    special_ability = models.ForeignKey(SpecialAbility, on_delete=models.CASCADE, related_name='species_abilities')

    def __str__(self):
        return f"{self.species.species_name} - {self.special_ability.ability_name}"
