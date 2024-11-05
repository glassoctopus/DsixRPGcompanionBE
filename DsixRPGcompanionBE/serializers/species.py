from rest_framework import serializers
from DsixRPGcompanionBE.models import Species

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = (
            'id',
            'uid',
            'playable',
            'image',
            'species_name',
            'species_homeworld',
            'species_average_height',
            'species_average_weight',
            'species_force_sensitive',
            'species_dexterity',
            'species_knowledge',
            'species_mechanical',
            'species_perception',
            'species_strength',
            'species_technical',
            'species_force_control',
            'species_force_sense',
            'species_force_alter',
            'species_force_points',
            'species_dark_side_points',
            'species_physical_description',
            'species_personality',
            'species_background',
            'species_force_strength',
            'species_appeared_in'
        )
