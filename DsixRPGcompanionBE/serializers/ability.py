from rest_framework import serializers
from DsixRPGcompanionBE.models.ability import Ability

class NameOfSpeciesOfAbility(serializers.ModelSerializer):
    # Lazy import to avoid circular import issues
    class Meta:
        from .species import Species  # Lazy import
        model = Species
        fields = ['id', 'species_name']

class AbilitySerializer(serializers.ModelSerializer):
    ability_of_the_species = NameOfSpeciesOfAbility(read_only=True)
    species_name = serializers.CharField(source='species.name', read_only=True)
    
    class Meta:
        model = Ability
        fields = (
            'id',
            'attribute',
            'name',
            'time_taken',
            'is_a_reaction',
            'force_ability',
            'species_specific',
            'species_name',
            'ability_of_the_species',
            'notes',
            'modifiers',
            'use_notes',
            'game_notes',
            'code',
            'source',
            'home_brew'
        )

