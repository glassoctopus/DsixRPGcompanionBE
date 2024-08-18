from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from DsixRPGcompanionBE.models import Character, Skill, CharacterSkill, SkillSpecialization
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from .skills import SkillSerializer , SkillSpecializationSerializer
import json

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('id', 'uid', 'user', 'NPC', 'image', 'name', 'archetype', 'species', 'homeworld', 'gender', 'age', 'height', 'weight', 'physical_description', 'personality', 'background', 'objectives', 'a_quote', 'credits', 'force_sensitive', 'dexterity', 'knowledge', 'mechanical', 'perception', 'strength', 'technical', 'force_control', 'force_sense', 'force_alter', 'force_points', 'dark_side_points', 'force_strength')

class CharacterSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer()
    specializations = SkillSpecializationSerializer(many=True, read_only=True)
    
    class Meta:
        model = CharacterSkill
        fields = ('id', 'skill', 'skill_code', 'specializations')  
            
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
            serializer = CharacterSerializer(character, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Character.DoesNotExist:
            raise Response({"error": "Character not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        """DELETE that hero"""
        try:
            character = Character.objects.get(pk=pk)
            serializer = CharacterSerializer(character) 
            character.delete()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        except character.DoesNotExist:
            return Response({"error": "Character not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    #character skills below, need to see how to get rid of this csrf hack
    @csrf_exempt
    @require_http_methods(["POST"])
    def add_skill_to_character(request):
        """create a skill or list of skills and specilizations"""
        try:
            data = json.loads(request.body)

            # Ensure data is a list, even if it's a single item
            if isinstance(data, dict):
                data = [data]
            elif not isinstance(data, list):
                return HttpResponseBadRequest("Invalid input data. Expected a dictionary or a list of skills.")

            created_character_skills = []
            errors = []

            for skill_data in data:
                if not isinstance(skill_data, dict):
                    errors.append(f"Invalid data format: {skill_data}")
                    continue

                character_id = skill_data.get('character')
                skill_id = skill_data.get('skill')
                skill_name = skill_data.get('skill_name')
                skill_code = skill_data.get('skill_code')
                specializations = skill_data.get('specializations', [])

                if not character_id or not (skill_id or skill_name) or skill_code is None:
                    errors.append(f"Invalid data for skill: {skill_data}")
                    continue

                try:
                    character = Character.objects.get(id=character_id)
                except Character.DoesNotExist:
                    errors.append(f"Character with ID {character_id} not found.")
                    continue

                try:
                    if skill_name:
                        skill = Skill.objects.get(skill_name=skill_name)
                    elif skill_id:
                        skill = Skill.objects.get(id=skill_id)
                    else:
                        raise Skill.DoesNotExist
                except Skill.DoesNotExist:
                    errors.append(f"Skill with ID {skill_id} or name {skill_name} not found.")
                    continue

                # Add or update the skill for the character
                character_skill, created = CharacterSkill.objects.update_or_create(
                    character=character,
                    skill=skill,
                    defaults={'skill_code': skill_code}
                )

                # Create or update the skill specializations if applicable
                if isinstance(specializations, list):
                    for specialization in specializations:
                        if not isinstance(specialization, dict):
                            errors.append(f"Invalid data format for specialization: {specialization}")
                            continue
                        
                        specialization_name = specialization.get('specialization_name')
                        specialization_code = specialization.get('specialization_code')

                        if specialization_name:
                            spec, spec_created = SkillSpecialization.objects.update_or_create(
                                character_skill=character_skill,
                                specialization_name=specialization_name,
                                defaults={'specialization_code': specialization_code}
                            )

                created_character_skills.append({
                    "character_skill_id": character_skill.id,
                    "skill_id": skill.id,
                    "skill_name": skill.skill_name,
                    "skill_code": skill_code,
                    "specializations": [
                        {
                            "specialization_id": spec.id,
                            "specialization_name": spec.specialization_name,
                            "specialization_code": spec.specialization_code
                        }
                        for spec in SkillSpecialization.objects.filter(character_skill=character_skill)
                    ]
                })
                
            response_data = {
                "message": f"Successfully added {len(created_character_skills)} skills to the character.",
                "created_skills": created_character_skills
            }
            if errors:
                response_data["errors"] = errors
            return JsonResponse(response_data, status=201)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format.")
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


    def retrieve_character_with_skills(self, request, character_id):
        """GET / Retrieve a character with associated skills"""
        try:
            character = get_object_or_404(Character, id=character_id)
            character_skills = CharacterSkill.objects.filter(character=character)
            
            # Serialize the character data
            character_serializer = CharacterSerializer(character)
            
            # Serialize the character skills
            character_skills_serializer = CharacterSkillSerializer(character_skills, many=True)
            
            # Prepare the response data
            response_data = {
                'character': character_serializer.data,
                'skills': character_skills_serializer.data
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Character.DoesNotExist:
            return Response({'error': 'Character not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['patch'], url_path='update-skill-code')
    def update_skill_code(self, request, pk=None):
        """PATCH /heros/{id}/update-skill-code/ Update skill_code for a character-skill relation"""
        try:
            data = request.data
            character_id = pk
            skill_id = data.get('skill_id')
            new_skill_code = data.get('skill_code')

            if not skill_id or new_skill_code is None:
                return HttpResponseBadRequest("Invalid input data. 'skill_id' and 'skill_code' are required.")

            try:
                character_skill = CharacterSkill.objects.get(character_id=character_id, skill_id=skill_id)
            except CharacterSkill.DoesNotExist:
                return HttpResponseNotFound("CharacterSkill relationship not found.(CharacterSkill.DoesNotExist:)")

            # Update skill_code
            character_skill.skill_code = new_skill_code
            character_skill.save()

            return JsonResponse({"message": "Skill code updated successfully!"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def remove_skill_from_character(self, request, character_id, skill_id):
        """DELETE a skill from a character"""
        try:
            CharacterSkill.objects.filter(character_id=character_id, skill_id=skill_id).delete()
            return Response({"message": "Skill removed successfully."}, status=status.HTTP_204_NO_CONTENT)
        except CharacterSkill.DoesNotExist:
            return Response({"error": "Skill not found for this character."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    