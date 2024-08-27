from rest_framework import serializers
from DsixRPGcompanionBE.models.skill import Skill

class SkillSerializer(serializers.ModelSerializer):
    """super serial"""
    skill_code = serializers.DecimalField(max_digits=2, decimal_places=1, coerce_to_string=False)
    class Meta:
        model = Skill
        fields = ('id',                  
                  'attribute', 
                  'skill_name', 
                  'time_taken', 
                  'is_a_reaction', 
                  'force_skill', 
                  'specializations_notes', 
                  'modifiers', 
                  'skill_use_notes', 
                  'skill_game_notes', 
                  'skill_code')

