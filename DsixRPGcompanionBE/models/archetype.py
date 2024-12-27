from django.core.exceptions import ValidationError
from django.db import models
from .species import Species

class Archetype(models.Model):
    archetype_name = models.CharField(max_length=113)
    archetype_for_NPC = models.BooleanField(default=False)
    archetype_force_sensitive = models.BooleanField(default=False, blank=True)
    archetype_dexterity = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    archetype_knowledge = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    archetype_mechanical = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    archetype_perception = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    archetype_strength = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    archetype_technical = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    archetype_force_control = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    archetype_force_sense = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    archetype_force_alter = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    archetype_starting_credits = models.IntegerField(default=0, blank=True, null=True)
    archetype_personality = models.CharField(max_length=1369, blank=True)
    archetype_background = models.CharField(max_length=1369, blank=True)
    archetype_objectives = models.CharField(max_length=1369, blank=True)
    archetype_a_quote = models.CharField(max_length=1369, blank=True)
    archetype_allowed_species = models.ManyToManyField('Species', blank=True, related_name='archetypes')
    archetype_game_notes = models.CharField(max_length=3666, null=True, blank=True)
    archetype_source = models.CharField(max_length=1369, null=True, blank=True)

    def clean(self):
        if not self.archetype_for_NPC:
            required_fields = [
                'archetype_force_sensitive',
                'archetype_dexterity',
                'archetype_knowledge',
                'archetype_mechanical',
                'archetype_perception',
                'archetype_strength',
                'archetype_technical',
                'archetype_force_control',
                'archetype_force_sense',
                'archetype_force_alter',
                'archetype_starting_credits',
                'archetype_personality',
                'archetype_background',
                'archetype_objectives',
                'archetype_a_quote',
                'archetype_game_notes',
                'archetype_source'
            ]
            
            for field in required_fields:
                value = getattr(self, field)
                if value in [None, '']:
                    raise ValidationError(f"{field} is required when archetype_for_NPC is False.")
        super().clean()

    def __str__(self):
        return self.archetype_name
    
    def allowed_species(self, species_name):
        """This is a design decesion that enforces canon and source archetypes that are species specific i.e. the Ewok archetypes in the first edition, but not covered in any rule sources"""
        if not self.archetype_allowed_species.exists():
            return True
        return self.archetype_allowed_species.filter(species_name=species_name).exists()
