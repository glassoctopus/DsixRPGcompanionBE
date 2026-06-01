from rest_framework import serializers
from ..models.equipment_feature_code import EquipmentFeatureCode


class EquipmentFeatureCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentFeatureCode
        fields = '__all__'