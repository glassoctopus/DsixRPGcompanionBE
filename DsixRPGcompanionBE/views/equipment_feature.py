from rest_framework import viewsets
from ..models.equipment_feature import EquipmentFeature
from ..serializers.equipment_feature import EquipmentFeatureSerializer


class EquipmentFeatureViewSet(viewsets.ModelViewSet):
    queryset = EquipmentFeature.objects.all()
    serializer_class = EquipmentFeatureSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        equipment_id = self.request.query_params.get('equipment', None)
        if equipment_id:
            queryset = queryset.filter(equipment_id=equipment_id)
        feature_type_id = self.request.query_params.get('feature_type', None)
        if feature_type_id:
            queryset = queryset.filter(feature_type_id=feature_type_id)
        return queryset