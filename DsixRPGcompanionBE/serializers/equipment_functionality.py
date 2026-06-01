from rest_framework import serializers
from ..models.equipment_functionality import EquipmentFunctionality
from ..serializers.equipment_functionality_code import EquipmentFunctionalityCodeSerializer


class EquipmentFunctionalitySerializer(serializers.ModelSerializer):
    values = EquipmentFunctionalityCodeSerializer(many=True, read_only=True)
    
    class Meta:
        model = EquipmentFunctionality
        fields = '__all__'