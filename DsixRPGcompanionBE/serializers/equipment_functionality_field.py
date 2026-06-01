from rest_framework import serializers
from ..models.equipment_functionality_field import EquipmentFunctionalityField


class FunctionalityFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentFunctionalityField
        fields = '__all__'