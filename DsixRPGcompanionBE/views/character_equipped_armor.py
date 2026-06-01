from rest_framework import viewsets
from ..models.character_equipped_armor import CharacterEquippedArmor
from ..serializers.character_equipped_armor import CharacterEquippedArmorSerializer


class EquippedArmorViewSet(viewsets.ModelViewSet):
    queryset = CharacterEquippedArmor.objects.all()
    serializer_class = CharacterEquippedArmorSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        character_id = self.request.query_params.get('character', None)
        if character_id:
            queryset = queryset.filter(character_id=character_id)
        return queryset