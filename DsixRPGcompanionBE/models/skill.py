from django.db import models

class Skill(models.Model):
    attribute = models.CharField(max_length=69)
    skill_name = models.CharField(max_length=69)
    time_taken = models.CharField(max_length=369, null=True, blank=True)
    is_a_reaction = models.BooleanField(default=False)
    force_skill = models.BooleanField(default=False)
    species_specific = models.BooleanField(default=False)
    species = models.ForeignKey('Species', related_name='skills', on_delete=models.CASCADE, null=True, blank=True)
    specializations_notes = models.CharField(max_length=3666, null=True, blank=True)
    modifiers = models.CharField(max_length=3666, null=True, blank=True)
    skill_use_notes = models.CharField(max_length=3666, null=True, blank=True)
    skill_game_notes = models.CharField(max_length=3666, null=True, blank=True)
    skill_code = models.DecimalField(max_digits=3, decimal_places=1)
    skill_source = models.CharField(max_length=1369, null=True, blank=True)
    home_brew = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.skill_name} (code {self.skill_code})"
