from rest_framework import serializers
from DsixRPGcompanionBE.models.character import Character
from DsixRPGcompanionBE.serializers.character_skill import CharacterSkillSerializer
from DsixRPGcompanionBE.serializers.skill_specialization import SkillSpecializationSerializer

class CharacterSerializer(serializers.ModelSerializer):
    character_skills = CharacterSkillSerializer(many=True, read_only=True)
    species_name = serializers.CharField(source='species.species_name', read_only=True)
    dexterity = serializers.DecimalField(max_digits=3, decimal_places=1)
    knowledge = serializers.DecimalField(max_digits=3, decimal_places=1)
    mechanical = serializers.DecimalField(max_digits=3, decimal_places=1)
    perception = serializers.DecimalField(max_digits=3, decimal_places=1)
    strength = serializers.DecimalField(max_digits=3, decimal_places=1)
    technical = serializers.DecimalField(max_digits=3, decimal_places=1)
    force_control = serializers.DecimalField(max_digits=3, decimal_places=1)
    force_sense = serializers.DecimalField(max_digits=3, decimal_places=1)
    force_alter = serializers.DecimalField(max_digits=3, decimal_places=1)
    user_handle = serializers.SerializerMethodField()
    archetype_name = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = ('id', 
                  'uid', 
                  'user',
                  'user_handle',
                  'NPC', 
                  'image', 
                  'name', 
                  'archetype',
                  'archetype_name',
                  'species',
                  'species_name',
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
          
    def get_user_handle(self, obj):
        return obj.user_handle
    
    def get_archetype_name(self, obj):
        return obj.archetype_name


