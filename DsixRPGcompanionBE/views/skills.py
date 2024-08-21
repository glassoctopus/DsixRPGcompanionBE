from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from DsixRPGcompanionBE.models import Skill, SkillSpecialization
from DsixRPGcompanionBE.serializers.skill import SkillSerializer

                
class SkillView(ViewSet):
    """skill API endpoint for CRUD"""
    def create(self, request, *args, **kwargs):
        data = request.data
        
        if isinstance(data, list):
            created_skills = []
            how_many = 0
            for skill in data:
                serializer = SkillSerializer(data=skill)
                if serializer.is_valid():
                    skill = serializer.save()
                    created_skills.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            how_many = len(created_skills)
            return Response({"message": f"There were {how_many} entries in this request to create skills. Here is that list", "created_skills": created_skills}, status=status.HTTP_201_CREATED)
        else:
            serializer = SkillSerializer(data=data)
            if serializer.is_valid():
                skill = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """get a single skill"""
        try:
            skill = Skill.objects.get(pk=pk)
            serializer = SkillSerializer(skill)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except skill.DoesNotExist:
            raise NotFound(detail="skill not found.", code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    def list(self, requests):
        """list all skills"""
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        """update a skill"""
        try:
            skill = Skill.objects.get(pk=pk)
            serializer = SkillSerializer(skill, data = request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except skill.DoesNotExist:
            raise Response({"error": "Skill not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        """DELETE this skill and return the deleted row"""
        try:
            skill = Skill.objects.get(pk=pk)
            serializer = SkillSerializer(skill) 
            skill.delete()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        except Skill.DoesNotExist:
            return Response({"error": "Skill not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
