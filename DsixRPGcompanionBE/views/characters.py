from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from DsixRPGcompanionBE.models import Character, Skill, CharacterSkill
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .skills import SkillSerializer 
import json

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
    
    @csrf_exempt    
    @require_http_methods(["POST"])
    def add_skill_to_character(request):
        try:
            data = json.loads(request.body)
            character_id = data.get('character')
            skill_id = data.get('skill')
            skill_code = data.get('skill_code')

            if not character_id or not skill_id or skill_code is None:
                return HttpResponseBadRequest("Invalid input data.")

            try:
                character = Character.objects.get(id=character_id)
                skill = Skill.objects.get(id=skill_id)
            except ObjectDoesNotExist:
                return HttpResponseNotFound("Character or Skill not found.")

            character_skill = CharacterSkill.objects.create(character=character, skill=skill, skill_code=skill_code)
            
            return JsonResponse({"message": "Skill added to character successfully!", "character_skill_id": character_skill.id})

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format.")
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


    def retrieve_character_with_skills(self, request, character_id):
        """GET / Retrieve a character with associated skills"""
        try:
            character = get_object_or_404(Character, id=character_id)
            character_skills = CharacterSkill.objects.filter(character=character)

            character_serializer = CharacterSerializer(character)

            skills = [skill.skill for skill in character_skills]
            skills_serializer = SkillSerializer(skills, many=True)
            
            # Prepare the response data
            response_data = {
                'character': character_serializer.data,
                'skills': skills_serializer.data
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Character.DoesNotExist:
            return Response({'error': 'Character not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def remove_skill_from_character(self, request, character_id, skill_id):
        """DELETE a skill from a character"""
        try:
            CharacterSkill.objects.filter(character_id=character_id, skill_id=skill_id).delete()
            return Response({"message": "Skill removed successfully."}, status=status.HTTP_204_NO_CONTENT)
        except CharacterSkill.DoesNotExist:
            return Response({"error": "Skill not found for this character."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    