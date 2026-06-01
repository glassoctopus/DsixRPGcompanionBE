from rest_framework import serializers
from ..models.character_equipment import CharacterEquipment


class CharacterEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterEquipment
        fields = '__all__'
        read_only_fields = ['acquired_date', 'last_modified']