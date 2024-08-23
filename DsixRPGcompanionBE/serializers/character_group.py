from rest_framework import serializers
from DsixRPGcompanionBE.models import CharacterGroup, Character

class CharacterGroupCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('id', 'user', 'name', 'archetype', 'NPC')
        
class CharacterGroupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CharacterGroup
        fields = ('id', 'user', 'group_name', 'game_master', 'characters', 'private', 'is_adventure_party')

    def create(self, validated_data):
        user_group = CharacterGroup.objects.create(**validated_data)
        return user_group