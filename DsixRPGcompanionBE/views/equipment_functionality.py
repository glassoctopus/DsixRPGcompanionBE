from rest_framework import viewsets
from ..models.equipment_functionality import EquipmentFunctionality
from ..serializers.equipment_functionality import EquipmentFunctionalitySerializer


class EquipmentFunctionalityViewSet(viewsets.ModelViewSet):
    queryset = EquipmentFunctionality.objects.all()
    serializer_class = EquipmentFunctionalitySerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        equipment_id = self.request.query_params.get('equipment', None)
        if equipment_id:
            queryset = queryset.filter(equipment_id=equipment_id)
        functionality_type_id = self.request.query_params.get('functionality_type', None)
        if functionality_type_id:
            queryset = queryset.filter(functionality_type_id=functionality_type_id)
        return queryset