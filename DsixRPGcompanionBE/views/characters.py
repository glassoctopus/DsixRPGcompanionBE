from django.http import HttpResponseServerError, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from DsixRPGcompanionBE.models import Character, Skill, CharacterSkill, SkillSpecialization
from DsixRPGcompanionBE.serializers.character import CharacterSerializer
from DsixRPGcompanionBE.serializers.character_skill import CharacterSkillSerializer
import json

class CharacterView(ViewSet): 
    
    def create(self, request, *args, **kwargs):
        """POST / Create hero(s)"""
        data = request.data 
        
        if isinstance(data, list): 
            created_character = []
            how_many = 0
            for hero in data:
                serializer = CharacterSerializer(data=hero)
                if serializer.is_valid():
                    hero = serializer.save()
                    created_character.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            how_many = len(created_character)
            return Response({"": f"There were {how_many} entries in this request to create Characters / Heros. Here is that list", "Characters added:": created_character}, status=status.HTTP_201_CREATED)
        else:
            serializer = CharacterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk):
        """get a single hero"""
        try:
            character = Character.objects.prefetch_related(
                Prefetch('character_skills__skill', to_attr='prefetched_skills'),
                Prefetch('character_skills__specializations', to_attr='prefetched_specializations')
            ).get(pk=pk)
            serializer = CharacterSerializer(character)
            return Response(serializer.data, status=status.HTTP_200_OK)            
        except Character.DoesNotExist:
            return NotFound(detail="Character not found.", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        """list all characters"""
        characters = Character.objects.all()
        how_many = characters.count()  
        in_the_toy_box = CharacterSerializer(characters, many=True)
        # return Response(in_the_toy_box.data, status=status.HTTP_200_OK)
        return Response({"message": f"We're gettng all {how_many} heros in your toy box out!", "They are":in_the_toy_box.data}, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        """Put / Update"""
        try:
            character = Character.objects.get(pk=pk)
            serializer = CharacterSerializer(character, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Character.DoesNotExist:
            raise Response({"error": "Character not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        """DELETE that hero"""
        try:
            character = Character.objects.get(pk=pk)
            if character.archetype is not None:
                print("Archetype associated:", character.archetype)
            serializer = CharacterSerializer(character)
            print("serializer, instance id:", serializer.data.keys())
            character.delete()
            print('Character "deleted" successfully')
            return Response(serializer.data, status=status.HTTP_200_OK) 
        except Character.DoesNotExist:
            return Response({"error": "Character not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post', 'put'], url_path='add-or-update-character-skills')
    def add_or_update_character_skills(self, request, *args, **kwargs):
        """Create or update a batch of skills and their specializations for a character."""
        try:
            data = request.data

            if isinstance(data, dict):
                data = [data]
            elif not isinstance(data, list):
                return HttpResponseBadRequest("Invalid input data. Expected a dictionary or a list of skills.")

            updated_skills = []
            errors = []

            # Print to debug the request method
            print(f"Request method: {request.method}")  # Debug line

            for skill_data in data:
                if not isinstance(skill_data, dict):
                    errors.append(f"Invalid data format: {skill_data}")
                    continue

                character_id = skill_data.get('character')
                skill_name = skill_data.get('skill_name')
                skill_code = skill_data.get('skill_code')
                specializations = skill_data.get('specializations', [])

                if not character_id or not skill_name or skill_code is None:
                    errors.append(f"Invalid data for skill: {skill_data}")
                    continue

                try:
                    character = Character.objects.get(id=character_id)
                except Character.DoesNotExist:
                    errors.append(f"Character with ID {character_id} not found.")
                    continue

                try:
                    skill = Skill.objects.get(skill_name=skill_name)
                except Skill.DoesNotExist:
                    errors.append(f"Skill with name {skill_name} not found.")
                    continue

                character_skill = None

                if request.method == "POST":
                    # Create logic: only create if method is POST
                    print("Handling POST logic for creation")  # Debug line
                    character_skill, created = CharacterSkill.objects.get_or_create(
                        character=character,
                        skill=skill,
                        defaults={'skill_code': skill_code, 'attribute': skill.attribute}
                    )

                    if not created:
                        errors.append(f"Skill '{skill_name}' already exists for the character with ID {character_id}.")
                        continue

                elif request.method == "PUT":
                    # Update logic: only update if method is PUT
                    print("Handling PUT logic for updating")  # Debug line
                    try:
                        character_skill = CharacterSkill.objects.get(character=character, skill=skill)
                        character_skill.skill_code = skill_code
                        character_skill.save()
                    except CharacterSkill.DoesNotExist:
                        errors.append(f"Skill '{skill_name}' not found for character with ID {character_id}.")
                        continue

                # Handle specializations if provided
                if character_skill:
                    if isinstance(specializations, list):
                        for specialization in specializations:
                            if not isinstance(specialization, dict):
                                errors.append(f"Invalid specialization format: {specialization}")
                                continue

                            specialization_name = specialization.get('specialization_name')
                            specialization_code = specialization.get('specialization_code')

                            if specialization_name:
                                SkillSpecialization.objects.update_or_create(
                                    character_skill=character_skill,
                                    specialization_name=specialization_name,
                                    defaults={'specialization_code': specialization_code}
                                )

                    # Append updated or created skill to response data
                    updated_skills.append({
                        "id": character_skill.id,
                        "character": character_id,
                        "skill": skill.id,
                        "skill_name": skill.skill_name,
                        "skill_code": character_skill.skill_code,
                        "attribute": character_skill.attribute,
                        "specializations": [
                            {
                                "id": spec.id,
                                "specialization_name": spec.specialization_name,
                                "specialization_code": spec.specialization_code
                            }
                            for spec in SkillSpecialization.objects.filter(character_skill=character_skill)
                        ]
                    })

            response_data = {
                "message": f"Successfully processed {len(updated_skills)} skills for the character.",
                "updated_skills": updated_skills
            }
            if errors:
                response_data["errors"] = errors

            return JsonResponse(response_data, status=200 if request.method == "PATCH" else 201)

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON format.")
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    
    @action(detail=True, methods=['get'], url_path='skills')
    def get_skills_for_character(self, request, pk=None):
        """GET all skills for a specific character"""
        try:
            character = get_object_or_404(Character, pk=pk)
            character_skills = CharacterSkill.objects.filter(character_id=pk)
            serializer = CharacterSkillSerializer(character_skills, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)     
        except CharacterSkill.DoesNotExist:
            return Response({"error": "No skills found for this character."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
    
    @action(detail=True, methods=['delete'], url_path='skills/(?P<skill_id>[^/.]+)')
    def remove_skill_from_character(self, request, pk=None, skill_id=None):
        """DELETE a skill from a character"""
        try:
            # pk is the character_id
            character_skill = CharacterSkill.objects.get(character_id=pk, skill_id=skill_id)
            character_skill.delete()
            return Response({"message": "Skill removed successfully."}, status=status.HTTP_204_NO_CONTENT)
        except CharacterSkill.DoesNotExist:
            return Response({"error": "Skill not found for this character."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    