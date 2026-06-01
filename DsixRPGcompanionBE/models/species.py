from django.db import models
class Species(models.Model):
    uid = models.CharField(max_length=113, unique=True)
    playable = models.BooleanField(default=False)
    image = models.CharField(max_length=223, null=True, blank=True)
    name = models.CharField(max_length=69, null=True, blank=True)
    homeworld = models.CharField(max_length=69, null=True, blank=True)
    average_height = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
    average_weight = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)
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
    physical_description = models.CharField(max_length=3696, null=True, blank=True)
    personality = models.CharField(max_length=3696, null=True, blank=True)
    background = models.CharField(max_length=3696, null=True, blank=True)
    force_strength = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    appeared_in = models.CharField(max_length=2369, null=True, blank=True)
    
    def __str__(self):
        return self.name
