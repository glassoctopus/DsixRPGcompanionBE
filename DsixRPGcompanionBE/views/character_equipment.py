from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models.character_equipment import CharacterEquipment
from ..serializers.character_equipment import CharacterEquipmentSerializer


class CharacterEquipmentViewSet(viewsets.ModelViewSet):
    queryset = CharacterEquipment.objects.all()
    serializer_class = CharacterEquipmentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        character_id = self.request.query_params.get('character', None)
        if character_id:
            queryset = queryset.filter(character_id=character_id)
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset
    
    @action(detail=True, methods=['post'])
    def equip(self, request, pk=None):
        character_equipment = self.get_object()
        character_equipment.status = 'equipped'
        character_equipment.save()
        return Response({'status': 'equipped'})
    
    @action(detail=True, methods=['post'])
    def store(self, request, pk=None):
        character_equipment = self.get_object()
        character_equipment.status = 'stored'
        character_equipment.save()
        return Response({'status': 'stored'})