from rest_framework import viewsets
from ..models.equipment_feature_field import EquipmentFeatureField
from ..serializers.equipment_feature_field import EquipmentFeatureFieldSerializer


class FeatureFieldViewSet(viewsets.ModelViewSet):
    queryset = EquipmentFeatureField.objects.all()
    serializer_class = EquipmentFeatureFieldSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        feature_type_id = self.request.query_params.get('feature_type', None)
        if feature_type_id:
            queryset = queryset.filter(feature_type_id=feature_type_id)
        return queryset