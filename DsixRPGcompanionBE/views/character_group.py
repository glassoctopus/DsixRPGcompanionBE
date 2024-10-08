from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.viewsets import ViewSet
from DsixRPGcompanionBE.models import CharacterGroup, Character, User
from DsixRPGcompanionBE.serializers import CharacterGroupSerializer
        
class CharacterGroupView(ViewSet):
    """CRUD on User Groups, and anccilary features for manipulating group elements"""

    def create(self, request):
        serializer = CharacterGroupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        character_groups = CharacterGroup.objects.all()
        serializer = CharacterGroupSerializer(character_groups, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            character_group = CharacterGroup.objects.get(pk=pk)
        except CharacterGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CharacterGroupSerializer(character_group)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            character_group = CharacterGroup.objects.get(pk=pk)
        except CharacterGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CharacterGroupSerializer(character_group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            character_group = CharacterGroup.objects.get(pk=pk)
            serializer = CharacterGroupSerializer(character_group)
        except CharacterGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        character_group.delete()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def add_character(self, request, pk=None):
        try:
            character_group = CharacterGroup.objects.get(pk=pk)
        except CharacterGroup.DoesNotExist:
            return Response({"error": "User group not found."}, status=status.HTTP_404_NOT_FOUND)

        character_id = request.data.get('character_id')
        if not character_id:
            return Response({"error": "Character ID not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            character = Character.objects.get(id=character_id)
        except Character.DoesNotExist:
            return Response({"error": "Character not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if character in character_group.characters.all():
            return Response({"error": "Character is already in the group."}, status=status.HTTP_400_BAD_REQUEST)
        
        character_group.characters.add(character)
        character_group.save()
        
        return Response(CharacterGroupSerializer(character_group).data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def add_characters(self, request, pk=None):
        try:
            character_group = CharacterGroup.objects.get(pk=pk)
        except CharacterGroup.DoesNotExist:
            return Response({"error": "User group not found."}, status=status.HTTP_404_NOT_FOUND)

        character_ids = request.data.get('character_ids', [])
        if not character_ids:
            return Response({"error": "No character IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        added_characters = []
        not_found_characters = []
        
        for character_id in character_ids:
            try:
                character = Character.objects.get(id=character_id)
                if character not in character_group.characters.all():
                    character_group.characters.add(character)
                    added_characters.append(character_id)
                else:
                    return Response({"error": f"Character with ID {character_id} is already in the group."}, status=status.HTTP_400_BAD_REQUEST)
            except Character.DoesNotExist:
                not_found_characters.append(character_id)

        if not_found_characters:
            return Response({"error": f"Characters with IDs {', '.join(map(str, not_found_characters))} not found."}, status=status.HTTP_404_NOT_FOUND)

        character_group.save()
        
        return Response(CharacterGroupSerializer(character_group).data, status=status.HTTP_200_OK)

    
    def remove_character(self, request, pk=None):
        try:
            character_group = CharacterGroup.objects.get(pk=pk)
        except CharacterGroup.DoesNotExist:
            return Response({"error": "User group not found."}, status=status.HTTP_404_NOT_FOUND)
        
        character_id = request.data.get('character_id')
        try:
            character = Character.objects.get(id=character_id)
        except Character.DoesNotExist:
            return Response({"error": "Character not found."}, status=status.HTTP_404_NOT_FOUND)
        
        character_group.characters.remove(character)
        return Response(CharacterGroupSerializer(character_group).data, status=status.HTTP_200_OK)

    
    def remove_characters(self, request, pk=None):
        try:
            character_group = CharacterGroup.objects.get(pk=pk)
        except CharacterGroup.DoesNotExist:
            return Response({"error": "User group not found."}, status=status.HTTP_404_NOT_FOUND)

        character_ids = request.data.get('character_ids', [])
        if not character_ids:
            return Response({"error": "No character IDs provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        for character_id in character_ids:
            try:
                character = Character.objects.get(id=character_id)
                character_group.characters.remove(character)
            except Character.DoesNotExist:
                return Response({"error": f"Character with ID {character_id} not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(CharacterGroupSerializer(character_group).data, status=status.HTTP_200_OK)
    
    def assign_game_master(self, request, pk=None):
        try:
            character_group = CharacterGroup.objects.get(pk=pk)
        except CharacterGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        game_master_id = request.data.get('game_master')
        try:
            game_master = User.objects.get(pk=game_master_id)
        except User.DoesNotExist:
            return Response({"error": "Game Master does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        character_group.game_master = game_master
        character_group.save()
        return Response(CharacterGroupSerializer(character_group).data)
    
    #Stretch Goals adding users to the group
    
   