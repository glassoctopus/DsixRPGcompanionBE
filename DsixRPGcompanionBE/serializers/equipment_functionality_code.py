from rest_framework import serializers
from ..models.equipment_functionality_code import EquipmentFunctionalityCode


class EquipmentFunctionalityCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentFunctionalityCode
        fields = '__all__'