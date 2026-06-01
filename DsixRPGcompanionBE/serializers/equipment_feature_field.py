from rest_framework import serializers
from ..models.equipment_feature_field import EquipmentFeatureField


class EquipmentFeatureFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentFeatureField
        fields = '__all__'