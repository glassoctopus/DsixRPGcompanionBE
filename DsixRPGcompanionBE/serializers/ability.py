from rest_framework import serializers
from DsixRPGcompanionBE.models import Ability

class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = [
            'id',
            'attribute',
            'ability_name',
            'time_taken',
            'is_a_reaction',
            'force_ability',
            'species_specific',
            'ability_notes',
            'modifiers',
            'ability_use_notes',
            'ability_game_notes',
            'ability_code'
        ]
