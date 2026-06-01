from rest_framework import viewsets
from ..models.equipment_functionality_type import EquipmentFunctionalityType
from ..serializers.equipment_functionality_type import EquipmentFunctionalityTypeSerializer


class FunctionalityTypeViewSet(viewsets.ModelViewSet):
    queryset = EquipmentFunctionalityType.objects.all()
    serializer_class = EquipmentFunctionalityTypeSerializer