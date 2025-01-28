from django.db import models

class Ability(models.Model):
    attribute = models.CharField(max_length=69)
    ability_name = models.CharField(max_length=69)
    time_taken = models.CharField(max_length=369, null=True, blank=True)
    is_a_reaction = models.BooleanField(default=False)
    force_ability = models.BooleanField(default=False)
    species_specific = models.BooleanField(default=False)
    species = models.ForeignKey('Species', related_name='abilites', on_delete=models.CASCADE, null=True, blank=True)
    ability_notes = models.CharField(max_length=3666, null=True, blank=True)
    modifiers = models.CharField(max_length=3666, null=True, blank=True)
    ability_use_notes = models.CharField(max_length=3666, null=True, blank=True)
    ability_game_notes = models.CharField(max_length=3666, null=True, blank=True)
    ability_code = models.DecimalField(max_digits=3, decimal_places=1)
    ability_source = models.CharField(max_length=1369, null=True, blank=True)
    
    def __str__(self):
        return f"{self.skill_name} (code {self.skill_code})"
