from django.db import models

class Species(models.Model):
    uid = models.CharField(max_length=113, unique=True)
    playable = models.BooleanField(default=False)
    image = models.CharField(max_length=223, null=True, blank=True)
    name = models.CharField(max_length=69, null=True, blank=True)
    species_name = models.CharField(max_length=69, null=True, blank=True)
    species_homeworld = models.CharField(max_length=69, null=True, blank=True)
    species_average_height = models.CharField(max_length=13, null=True, blank=True)
    species_average_weight = models.CharField(max_length=13, null=True, blank=True)
    species_force_sensitive = models.BooleanField(default=False, null=True, blank=True)
    species_dexterity_modifer = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    species_knowledge = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    species_mechanical = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    species_perception = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    species_strength = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    species_technical = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    species_force_control = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    species_force_sense = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    species_force_alter = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    species_force_points = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    species_dark_side_points = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    species_physical_description = models.CharField(max_length=2369, null=True, blank=True)
    species_personality = models.CharField(max_length=2369, null=True, blank=True)
    species_background = models.CharField(max_length=2369, null=True, blank=True)
    species_force_strength = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    species_specific = models.BooleanField(default=False, null=True, blank=True)
    
    def __str__(self):
        return self.name
