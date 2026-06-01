from rest_framework import serializers
from ..models.character_equipped_armor import CharacterEquippedArmor


class CharacterEquippedArmorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterEquippedArmor
        fields = '__all__'