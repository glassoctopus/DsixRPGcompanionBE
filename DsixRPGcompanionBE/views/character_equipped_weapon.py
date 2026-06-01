from rest_framework import viewsets
from ..models.character_equipped_weapon import CharacterEquippedWeapon
from ..serializers.character_equipped_weapon import CharacterEquippedWeaponSerializer


class EquippedWeaponViewSet(viewsets.ModelViewSet):
    queryset = CharacterEquippedWeapon.objects.all()
    serializer_class = CharacterEquippedWeaponSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        character_id = self.request.query_params.get('character', None)
        if character_id:
            queryset = queryset.filter(character_id=character_id)
        return queryset