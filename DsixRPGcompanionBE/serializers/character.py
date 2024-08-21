from rest_framework import serializers
from DsixRPGcompanionBE.models.character import Character
from DsixRPGcompanionBE.serializers.character_skill import CharacterSkillSerializer
from DsixRPGcompanionBE.serializers.skill_specialization import SkillSpecializationSerializer

class CharacterSerializer(serializers.ModelSerializer):
    character_skills = CharacterSkillSerializer(many=True, read_only=True)
    class Meta:
        model = Character
        fields = ('id', 'uid', 'user', 'NPC', 'image', 'name', 'archetype', 'species', 'homeworld', 'gender', 'age', 'height', 'weight', 'physical_description', 'personality', 'background', 'objectives', 'a_quote', 'credits', 'force_sensitive', 'dexterity', 'knowledge', 'mechanical', 'perception', 'strength', 'technical', 'force_control', 'force_sense', 'force_alter', 'force_points', 'dark_side_points', 'force_strength', 'character_skills')


