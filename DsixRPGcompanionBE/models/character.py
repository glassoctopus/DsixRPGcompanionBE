from django.db import models
from .archetype import Archetype
from .species import Species
from .skill import Skill
from .user import User

class Character(models.Model):
    uid = models.CharField(max_length=113, unique=True)
    NPC = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='characters', null=True, blank=True)
    image = models.CharField(max_length=223, null=True, blank=True)
    name = models.CharField(max_length=69, null=True, blank=True)
    archetype = models.ForeignKey(Archetype, on_delete=models.CASCADE, related_name='archetypes', null=True, blank=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='characters', null=True, blank=True)
    homeworld = models.CharField(max_length=69, null=True, blank=True)
    gender = models.CharField(max_length=13, null=True, blank=True)
    age = models.IntegerField(default=21, null=True, blank=True)
    height = models.CharField(max_length=13, null=True, blank=True)
    weight = models.CharField(max_length=13, null=True, blank=True)
    force_sensitive = models.BooleanField(default=False, null=True, blank=True)
    dexterity = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    knowledge = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    mechanical = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    perception = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    strength = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    technical = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    force_control = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    force_sense = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    force_alter = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    force_points = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    dark_side_points = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    physical_description = models.CharField(max_length=2369, null=True, blank=True)
    personality = models.CharField(max_length=2369, null=True, blank=True)
    background = models.CharField(max_length=2369, null=True, blank=True)
    objectives = models.CharField(max_length=2369, null=True, blank=True)
    a_quote = models.CharField(max_length=2369, null=True, blank=True)
    credits = models.IntegerField(default=0, null=True, blank=True)
    force_strength = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    skill_points = models.IntegerField(default=0, null=True, blank=True)
    skills = models.ManyToManyField(Skill, through='CharacterSkill')
    
    def __str__(self):
        return self.name

    def character_header(self):
        return f"{self.name} (UID: {self.uid}, Handle: {self.user_handle if self.user else 'No User'})"

    @property
    def user_handle(self):
        return self.user.handle if self.user else 'No User'
    
    @property
    def archetype_name(self):
        return self.archetype.archetype_name if self.archetype else 'No Archetype'
    
    @property
    def species_name(self):
        return self.species.species_name if self.species else 'No Species'