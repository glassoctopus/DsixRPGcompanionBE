from rest_framework import serializers
from .models import SpeciesAbility

class SpeciesAbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeciesAbility
        fields = ['id', 'species', 'special_ability']
