from django.db import models

class Archetype(models.Model):
    archetype_name = models.CharField(max_length=113)
    archetype_force_sensitive = models.BooleanField(default=False)
    archetype_dexterity = models.DecimalField(max_digits=3, decimal_places=1)
    archetype_knowledge = models.DecimalField(max_digits=3, decimal_places=1)
    archetype_mechanical = models.DecimalField(max_digits=3, decimal_places=1)
    archetype_perception = models.DecimalField(max_digits=3, decimal_places=1)
    archetype_strength = models.DecimalField(max_digits=3, decimal_places=1)
    archetype_technical = models.DecimalField(max_digits=3, decimal_places=1)
    archetype_force_control = models.DecimalField(max_digits=3, decimal_places=1)
    archetype_force_sense = models.DecimalField(max_digits=3, decimal_places=1)
    archetype_force_alter = models.DecimalField(max_digits=3, decimal_places=1)
    archetype_starting_credits = models.IntegerField(default=0)
    archetype_personality = models.CharField(max_length=1369)
    archetype_background = models.CharField(max_length=1369)
    archetype_objectives = models.CharField(max_length=1369)
    archetype_a_quote = models.CharField(max_length=1369)
    archetype_game_notes = models.CharField(max_length=3666, null=True, blank=True)

    def __str__(self):
        return self.archetype_name
