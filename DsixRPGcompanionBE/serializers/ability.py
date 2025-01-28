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
    species_name = serializers.CharField(source='ability_of_the_species.species_name', read_only=True)
    
    class Meta:
        model = Ability
        fields = (
            'id',
            'attribute',
            'ability_name',
            'time_taken',
            'is_a_reaction',
            'force_ability',
            'species_specific',
            'species_name',
            'ability_of_the_species',
            'ability_notes',
            'modifiers',
            'ability_use_notes',
            'ability_game_notes',
            'ability_code',
            'ability_source',
        )

