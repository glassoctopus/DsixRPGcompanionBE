from rest_framework import serializers
from ..models.character_equipped_weapon import EquippedWeapon

class CharacterEquippedWeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquippedWeapon
        fields = '__all__'
        