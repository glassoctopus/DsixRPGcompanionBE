from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from DsixRPGcompanionBE.models import UserGroup, Character, User

class UserGroupCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('id', 'user', 'name', 'archetype', 'NPC')
        
class UserGroupUserSerializer(serializers.ModelSerializer):
    characters = UserGroupCharacterSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id',  'characters', 'game_master')
        
class UserGroupSerializer(serializers.ModelSerializer):
    users = UserGroupUserSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserGroup
        fields = ('id', 'group_name', 'users', 'private', 'is_adventure_party', 'game_master')

    def create(self, validated_data):
        user_group = UserGroup.objects.create(**validated_data)
        return user_group

        
class UserGroupView(ViewSet):
    """CRUD on User Groups, and anccilary features for manipulating group elements"""

    def create(self, request):
        serializer = UserGroupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        user_groups = UserGroup.objects.all()
        serializer = UserGroupSerializer(user_groups, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            user_group = UserGroup.objects.get(pk=pk)
        except UserGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserGroupSerializer(user_group)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            user_group = UserGroup.objects.get(pk=pk)
        except UserGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserGroupSerializer(user_group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            user_group = UserGroup.objects.get(pk=pk)
            serializer = UserGroupSerializer(user_group)
        except UserGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_group.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def add_user(self, request, pk=None):
        try:
            user_group = UserGroup.objects.get(pk=pk)
        except UserGroup.DoesNotExist:
            return Response({"error": "User group not found."}, status=status.HTTP_404_NOT_FOUND)

        user_id = request.data.get('user_id')

        if not user_id:
            return Response({"error": "No user ID provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user in user_group.users.all():
            return Response({"error": "User is already a member of this group."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_group.users.add(user)
            user_group.save() 
            return Response(UserGroupSerializer(user_group).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
    @action(detail=True, methods=['post'])
    def add_users(self, request, pk=None):
        try:
            user_group = UserGroup.objects.get(pk=pk)
        except UserGroup.DoesNotExist:
            return Response({"error": "User group not found."}, status=status.HTTP_404_NOT_FOUND)

        user_ids = request.data.get('user_ids', [])

        if not user_ids:
            return Response({"error": "No user IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(id__in=user_ids)

        if users.count() != len(user_ids):
            return Response({"error": "Some users not found."}, status=status.HTTP_404_NOT_FOUND)

        existing_users = user_group.users.all()
        new_users = users.exclude(id__in=existing_users.values_list('id', flat=True))

        if new_users:
            user_group.users.add(*new_users)
            user_group.save() 

        return Response(UserGroupSerializer(user_group).data)
    
    @action(detail=True, methods=['delete'], url_path='remove_user/(?P<user_id>[^/.]+)')
    def remove_user(self, request, pk=None, user_id=None):
        try:
            user_group = UserGroup.objects.get(pk=pk)
        except UserGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        user_group.users.remove(user)
        return Response(UserGroupSerializer(user_group).data)
    
    def remove_users(self, request, pk=None):
        try:
            user_group = UserGroup.objects.get(pk=pk)
        except UserGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        user_ids = request.data.get('user_ids', [])
        users = User.objects.filter(id__in=user_ids)
        user_group.users.remove(*users)
        return Response(UserGroupSerializer(user_group).data)
    
    @action(detail=True, methods=['post'])
    def add_character(self, request, pk=None):
        try:
            user_group = UserGroup.objects.get(pk=pk)
        except UserGroup.DoesNotExist:
            return Response({"error": "User group not found."}, status=status.HTTP_404_NOT_FOUND)

        character_id = request.data.get('character_id')
        if not character_id:
            return Response({"error": "Character ID not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            character = Character.objects.get(id=character_id)
        except Character.DoesNotExist:
            return Response({"error": "Character not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if character in user_group.characters.all():
            return Response({"error": "Character is already in the group."}, status=status.HTTP_400_BAD_REQUEST)
        
        user_group.characters.add(character)
        user_group.save()
        
        return Response(UserGroupSerializer(user_group).data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def add_characters(self, request, pk=None):
        try:
            user_group = UserGroup.objects.get(pk=pk)
        except UserGroup.DoesNotExist:
            return Response({"error": "User group not found."}, status=status.HTTP_404_NOT_FOUND)

        character_ids = request.data.get('character_ids', [])
        if not character_ids:
            return Response({"error": "No character IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        added_characters = []
        not_found_characters = []
        
        for character_id in character_ids:
            try:
                character = Character.objects.get(id=character_id)
                if character not in user_group.characters.all():
                    user_group.characters.add(character)
                    added_characters.append(character_id)
                else:
                    return Response({"error": f"Character with ID {character_id} is already in the group."}, status=status.HTTP_400_BAD_REQUEST)
            except Character.DoesNotExist:
                not_found_characters.append(character_id)

        if not_found_characters:
            return Response({"error": f"Characters with IDs {', '.join(map(str, not_found_characters))} not found."}, status=status.HTTP_404_NOT_FOUND)

        user_group.save()
        
        return Response(UserGroupSerializer(user_group).data, status=status.HTTP_200_OK)

    
    def remove_character(self, request, pk=None):
        try:
            user_group = UserGroup.objects.get(pk=pk)
        except UserGroup.DoesNotExist:
            return Response({"error": "User group not found."}, status=status.HTTP_404_NOT_FOUND)
        
        character_id = request.data.get('character_id')
        try:
            character = Character.objects.get(id=character_id)
        except Character.DoesNotExist:
            return Response({"error": "Character not found."}, status=status.HTTP_404_NOT_FOUND)
        
        user_group.characters.remove(character)
        return Response(UserGroupSerializer(user_group).data, status=status.HTTP_200_OK)

    
    def remove_characters(self, request, pk=None):
        try:
            user_group = UserGroup.objects.get(pk=pk)
        except UserGroup.DoesNotExist:
            return Response({"error": "User group not found."}, status=status.HTTP_404_NOT_FOUND)

        character_ids = request.data.get('character_ids', [])
        if not character_ids:
            return Response({"error": "No character IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        for character_id in character_ids:
            try:
                character = Character.objects.get(id=character_id)
                user_group.characters.remove(character)
            except Character.DoesNotExist:
                return Response({"error": f"Character with ID {character_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(UserGroupSerializer(user_group).data, status=status.HTTP_200_OK)
    
    def assign_game_master(self, request, pk=None):
        try:
            user_group = UserGroup.objects.get(pk=pk)
        except UserGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        game_master_id = request.data.get('game_master')
        try:
            game_master = User.objects.get(pk=game_master_id)
        except User.DoesNotExist:
            return Response({"error": "Game Master does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        user_group.game_master = game_master
        user_group.save()
        return Response(UserGroupSerializer(user_group).data)