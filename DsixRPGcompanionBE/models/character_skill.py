from django.db import models
from .character import Character
from .skill import Skill

class CharacterSkill(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='character_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='skill_characters')
    skill_code = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return f"{self.character.name} - {self.skill.skill_name} (code {self.skill_code})"
