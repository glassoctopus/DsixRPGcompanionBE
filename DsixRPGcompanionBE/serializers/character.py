from rest_framework import serializers
from DsixRPGcompanionBE.models.character import Character
from DsixRPGcompanionBE.serializers.character_skill import CharacterSkillSerializer
from DsixRPGcompanionBE.serializers.skill_specialization import SkillSpecializationSerializer

class CharacterSerializer(serializers.ModelSerializer):
    character_skills = CharacterSkillSerializer(many=True, read_only=True)
    dexterity = serializers.DecimalField(max_digits=3, decimal_places=1)
    knowledge = serializers.DecimalField(max_digits=3, decimal_places=1)
    mechanical = serializers.DecimalField(max_digits=3, decimal_places=1)
    perception = serializers.DecimalField(max_digits=3, decimal_places=1)
    strength = serializers.DecimalField(max_digits=3, decimal_places=1)
    technical = serializers.DecimalField(max_digits=3, decimal_places=1)
    force_control = serializers.DecimalField(max_digits=3, decimal_places=1)
    force_sense = serializers.DecimalField(max_digits=3, decimal_places=1)
    force_alter = serializers.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        model = Character
        fields = ('id', 
                  'uid', 
                  'user', 
                  'NPC', 
                  'image', 
                  'name', 
                  'archetype', 
                  'species', 
                  'homeworld', 
                  'gender', 
                  'age', 
                  'height', 
                  'weight', 
                  'physical_description', 
                  'personality', 
                  'background', 
                  'objectives', 
                  'a_quote', 
                  'credits', 
                  'force_sensitive', 
                  'dexterity', 
                  'knowledge', 
                  'mechanical', 
                  'perception', 
                  'strength', 
                  'technical', 
                  'force_control', 
                  'force_sense', 
                  'force_alter', 
                  'force_points', 
                  'dark_side_points', 
                  'force_strength', 
                  'character_skills')


