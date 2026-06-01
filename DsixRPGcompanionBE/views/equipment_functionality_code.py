from rest_framework import viewsets
from ..models.equipment_functionality_code import EquipmentFunctionalityCode
from ..serializers.equipment_functionality_code import EquipmentFunctionalityCodeSerializer


class EquipmentFunctionalityValueViewSet(viewsets.ModelViewSet):
    queryset = EquipmentFunctionalityCode.objects.all()
    serializer_class = EquipmentFunctionalityCodeSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        equipment_functionality_id = self.request.query_params.get('equipment_functionality', None)
        if equipment_functionality_id:
            queryset = queryset.filter(equipment_functionality_id=equipment_functionality_id)
        return queryset