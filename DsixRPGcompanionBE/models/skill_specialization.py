from django.db import models
from .character_skill import CharacterSkill

class SkillSpecialization(models.Model):
    character_skill = models.ForeignKey(CharacterSkill, on_delete=models.CASCADE, related_name='specializations')
    specialization_name = models.CharField(max_length=223)
    specialization_code = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return f"{self.specialization_name} (Code: {self.specialization_code}) for {self.character_skill.skill.skill_name} and {self.character_skill.character.name}"

    class Meta:
        verbose_name = "Skill Specialization"
        verbose_name_plural = "Skill Specializations"

