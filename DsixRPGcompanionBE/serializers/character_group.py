from rest_framework import serializers
from DsixRPGcompanionBE.models import CharacterGroup, Character, User

class CharacterGroupCharacterSerializer(serializers.ModelSerializer):
    user_handle = serializers.SerializerMethodField()
    archetype_name = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = ('id', 'user', 'user_handle', 'name', 'archetype_name', 'NPC')

    def get_user_handle(self, obj):
        return obj.user_handle
    
    def get_archetype_name(self, obj):
        return obj.archetype_name

class CharacterGroupSerializer(serializers.ModelSerializer):
    characters = CharacterGroupCharacterSerializer(many=True, read_only=True)
    user_handle = serializers.SerializerMethodField()
    game_master_handle = serializers.SerializerMethodField()
    
    # for future Thomas: to access as writable fields, removing them from the payload, the telling django to process them as a relationship and not an id value.
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    game_master = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)
    
    class Meta:
        model = CharacterGroup
        fields = ('id', 'user', 'user_handle', 'group_name', 'game_master', 'game_master_handle', 'characters', 'private', 'is_adventure_party')

    def create(self, validated_data):
        user = validated_data.pop('user')
        game_master = validated_data.pop('game_master', None)
        
        user_group = CharacterGroup.objects.create(user=user, game_master=game_master, **validated_data)
        return user_group
    
    def get_user_handle(self, obj):
        return obj.user_handle

    def get_game_master_handle(self, obj):
        return obj.game_master_user_handle if obj.game_master_user_handle else 'No GM Assigned'
