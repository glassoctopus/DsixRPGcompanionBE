from rest_framework import viewsets
from ..models.equipment_feature_type import EquipmentFeatureType
from ..serializers.equipment_feature_type import EquipmentFeatureTypeSerializer


class FeatureTypeViewSet(viewsets.ModelViewSet):
    queryset = EquipmentFeatureType.objects.all()
    serializer_class = EquipmentFeatureTypeSerializer