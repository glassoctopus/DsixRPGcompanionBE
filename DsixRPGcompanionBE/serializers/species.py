from rest_framework import serializers
from DsixRPGcompanionBE.models import Species

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = [
            'id',
            'name',
            'species_name',
            'species_homeworld',
            'species_average_height',
            'species_average_weight',
            'species_force_sensitive',
            'species_physical_description',
            'species_personality',
            'species_background',
            'image',
        ]
