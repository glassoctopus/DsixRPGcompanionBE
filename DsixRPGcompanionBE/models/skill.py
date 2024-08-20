from django.db import models

class Skill(models.Model):
    attribute = models.CharField(max_length=69)
    skill_name = models.CharField(max_length=69)
    time_taken = models.CharField(max_length=369, null=True, blank=True)
    is_a_reaction = models.BooleanField(default=False)
    force_skill = models.BooleanField(default=False)
    specializations_notes = models.CharField(max_length=3666, null=True, blank=True)
    modifiers = models.CharField(max_length=3666, null=True, blank=True)
    skill_use_notes = models.CharField(max_length=3666, null=True, blank=True)
    skill_game_notes = models.CharField(max_length=3666, null=True, blank=True)
    skill_code = models.DecimalField(max_digits=3, decimal_places=1)
    
    def __str__(self):
        return f"{self.skill_name} (code {self.skill_code})"
