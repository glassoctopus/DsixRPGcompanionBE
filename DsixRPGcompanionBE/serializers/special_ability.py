from rest_framework import serializers
from DsixRPGcompanionBE.models import SpecialAbility

class SpecialAbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialAbility
        fields = [
            'id',
            'ability_name',
            'attribute',
            'time_taken',
            'is_a_reaction',
            'force_skill',
            'species_specific',
            'special_ability_notes',
        ]
