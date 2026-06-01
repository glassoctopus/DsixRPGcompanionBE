from rest_framework import serializers
from DsixRPGcompanionBE.models.skill import Skill
from DsixRPGcompanionBE.models.species import Species

class NameOfSpeciesOfSkill(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ['id', 'species_name']

class SkillSerializer(serializers.ModelSerializer):
    """super serial"""
    code = serializers.DecimalField(max_digits=2, decimal_places=1, coerce_to_string=False)
    species = NameOfSpeciesOfSkill(read_only=True)
    species_name = serializers.CharField(source='species.species_name', read_only=True)

    class Meta:
        model = Skill
        fields = ('id',                  
                  'attribute', 
                  'name', 
                  'time_taken', 
                  'is_a_reaction', 
                  'force_skill', 
                  'specializations_notes',
                  'species_specific',
                  'species_name',
                  'species', 
                  'modifiers', 
                  'use_notes', 
                  'game_notes', 
                  'code',
                  )
  

