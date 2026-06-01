from rest_framework import viewsets
from ..models.equipment_feature_code import EquipmentFeatureCode
from ..serializers.equipment_feature_code import EquipmentFeatureCodeSerializer


class EquipmentFeatureValueViewSet(viewsets.ModelViewSet):
    queryset = EquipmentFeatureCode.objects.all()
    serializer_class = EquipmentFeatureCodeSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        equipment_feature_id = self.request.query_params.get('equipment_feature', None)
        if equipment_feature_id:
            queryset = queryset.filter(equipment_feature_id=equipment_feature_id)
        return queryset