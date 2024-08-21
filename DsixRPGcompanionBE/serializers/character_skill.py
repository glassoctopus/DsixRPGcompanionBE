from rest_framework import serializers
from DsixRPGcompanionBE.models.character import Character
from DsixRPGcompanionBE.models.character_skill import CharacterSkill
from DsixRPGcompanionBE.serializers.skill_specialization import SkillSpecializationSerializer

class CharacterSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.skill_name', read_only=True)
    specializations = SkillSpecializationSerializer(many=True, read_only=True)
    
    class Meta:
        model = CharacterSkill
        fields = ('skill_name', 'skill_code', 'specializations')
        
