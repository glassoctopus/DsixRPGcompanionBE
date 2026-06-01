from django.core.exceptions import ValidationError
from django.db import models
from .species import Species

class Archetype(models.Model):
    name = models.CharField(max_length=113)
    for_NPC = models.BooleanField(default=False)
    force_sensitive = models.BooleanField(default=False, blank=True)
    playable = models.BooleanField(default=True, blank=False)
    imperial = models.BooleanField(default=False, blank=True)
    dexterity = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    knowledge = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    mechanical = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    perception = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    strength = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    technical = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    force_control = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    force_sense = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    force_alter = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    starting_credits = models.IntegerField(default=0, blank=True, null=True)
    personality = models.CharField(max_length=1369, blank=True)
    background = models.CharField(max_length=1369, blank=True)
    objectives = models.CharField(max_length=1369, blank=True)
    a_quote = models.CharField(max_length=1369, blank=True)
    allowed_species = models.ManyToManyField('Species', blank=True, related_name='archetypes')
    game_notes = models.CharField(max_length=3666, null=True, blank=True)
    source = models.CharField(max_length=1369, null=True, blank=True)

    def clean(self):
        if not self.for_NPC:
            required_fields = [
                'force_sensitive',
                'dexterity',
                'knowledge',
                'mechanical',
                'perception',
                'strength',
                'technical',
                'force_control',
                'force_sense',
                'force_alter',
                'starting_credits',
                'personality',
                'background',
                'objectives',
                'a_quote',
                'game_notes',
                'source'
            ]
            
            for field in required_fields:
                value = getattr(self, field)
                if value in [None, '']:
                    raise ValidationError(f"{field} is required when for_NPC is False.")
        super().clean()

    def __str__(self):
        return self.name
    
    def allowed_species(self, species_name):
        """This is a design decesion that enforces canon and source archetypes that are species specific i.e. the Ewok archetypes in the first edition, but not covered in any rule sources"""
        if not self.allowed_species.exists():
            return True
        return self.allowed_species.filter(species_name=species_name).exists()
