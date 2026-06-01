from rest_framework import serializers
from ..models.character_equipped_gear import EquippedGear

class CharacterEquippedGearSeralizer(serializers.ModelSerializer):
    class Meta:
        model = EquippedGear
        fields = '__all__'