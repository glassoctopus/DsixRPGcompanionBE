from rest_framework import serializers
from ..models.equipment_feature import EquipmentFeature
from ..serializers.equipment_feature_code import EquipmentFeatureCodeSerializer


class EquipmentFeatureSerializer(serializers.ModelSerializer):
    values = EquipmentFeatureCodeSerializer(many=True, read_only=True)
    
    class Meta:
        model = EquipmentFeature
        fields = '__all__'