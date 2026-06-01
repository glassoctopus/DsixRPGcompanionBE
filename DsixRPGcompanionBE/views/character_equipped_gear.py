from rest_framework import viewsets
from ..models.character_equipped_gear import CharacterEquippedGear
from ..serializers.character_equipped_gear import CharacterEquippedGearSeralizer


class EquippedGearViewSet(viewsets.ModelViewSet):
    queryset = CharacterEquippedGear.objects.all()
    serializer_class = CharacterEquippedGearSeralizer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        character_id = self.request.query_params.get('character', None)
        if character_id:
            queryset = queryset.filter(character_id=character_id)
        slot_filter = self.request.query_params.get('slot', None)
        if slot_filter:
            queryset = queryset.filter(slot=slot_filter)
        return queryset