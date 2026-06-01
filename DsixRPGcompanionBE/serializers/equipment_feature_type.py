from rest_framework import serializers
from ..models.equipment_feature_type import EquipmentFeatureType


class EquipmentFeatureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentFeatureType
        fields = '__all__'