from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from DsixRPGcompanionBE.models import Character, Skill, CharacterSkill
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

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
    
    def destroy(self, pk):
        """DELETE that hero"""
        try:
            character = Character.objects.get(pk=pk)
            character.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Character.DoesNotExist:
            return Response({"error": "Character not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    @method_decorator(require_http_methods(["POST"]))
    def add_skill_to_character(request):
        character_id = request.POST.get('character_id')
        skill_id = request.POST.get('skill_id')
        skill_code = request.POST.get('skill_code')
        character = get_object_or_404(Character, id=character_id)
        skill = get_object_or_404(Skill, id=skill_id)
        character_skill, created = CharacterSkill.objects.get_or_create(
            character=character,
            skill=skill,
            defaults={'skill_code': skill_code}
        )
        if not created:
            character_skill.skill_code = skill_code
            character_skill.save()
        return JsonResponse({"message": "Skill added to character successfully!", "character_skill_id": character_skill.id})

    def remove_skill_from_character(character_id, skill_id):
        CharacterSkill.objects.filter(character_id=character_id, skill_id=skill_id).delete()
    
    