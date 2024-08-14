from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from DsixRPGcompanionBE.models import Character 

class CharacterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Character
        fields = ('uid', 'NPC', 'image', 'name', 'archetype', 'species', 'homeworld', 'gender', 'age', 'height', 'weight', 'physical_description', 'personality', 'background', 'objectives', 'a_quote', 'credits', 'force_sensitive', 'dexterity', 'knowledge', 'mechanical', 'perception', 'strength', 'technical', 'force_control', 'force_sense', 'force_alter', 'force_points', 'dark_side_points', 'force_strength')

class CharacterView(ViewSet):
    
    def create(self, request):
        """POST / Create hero """
        serializer =  CharacterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk):
        """get a single hero"""
        try:
            character = Character.objects.get(pk=pk)
            serializer = CharacterSerializer(character)
            return Response(serializer.data, status=status.HTTP_200_OK)            
        except Character.DoesNotExist:
            return NotFound(detail="Character not found.", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """list all characters"""
        characters = Character.objects.all()
        serializer = CharacterSerializer(characters, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        """Put / Update"""
        try:
            character = Character.objects.get(pk=pk)
            serializer = CharacterSerializer(character, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Character.DoesNotExist:
            raise Response({"error": "Character not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        """DELETE that hero"""
        try:
            character = Character.objects.get(pk=pk)
            character.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Character.DoesNotExist:
            return Response({"error": "Character not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
    