from rest_framework import serializers
from ..models.equipment_functionality_type import EquipmentFunctionalityType

class EquipmentFunctionalityTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentFunctionalityType
        fields = '__all__'