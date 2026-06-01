from rest_framework import viewsets
from ..models.equipment_restriction_override import EquipmentRestrictionOverride
from ..serializers.equipment_restriction_override import EquipmentRestrictionOverrideSerializer


class EquipmentRestrictionOverrideViewSet(viewsets.ModelViewSet):
    queryset = EquipmentRestrictionOverride.objects.all()
    serializer_class = EquipmentRestrictionOverrideSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        character_id = self.request.query_params.get('character', None)
        if character_id:
            queryset = queryset.filter(character_id=character_id)
        return queryset