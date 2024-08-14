from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from DsixRPGcompanionBE.models import Skill 

class SkillSerializer(serializers.ModelSerializer):
    """super serial"""
    skill_code = serializers.DecimalField(max_digits=2, decimal_places=1, coerce_to_string=False)
    class Meta:
        model = Skill
        fields = ('id', 'attribute', 'skill_name', 'time_taken', 'is_a_reaction', 'force_skill', 'specializations', 'skill_use_notes', 'skill_game_notes', 'skill_code')
        
class SkillView(ViewSet):
    """skill API endpoint for CRUD"""
    def create(self, request, *args, **kwargs):
        data = request.data
        
        if isinstance(data, list):
            created_skills = []
            for item in data:
                serializer = SkillSerializer(data=item)
                if serializer.is_valid():
                    skill = serializer.save()
                    created_skills.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(created_skills, status=status.HTTP_201_CREATED)
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
            payload = request.data
            
            skill.skill_name = payload.get("skill_name", skill.skill_name)
            skill.skill_code = payload.get("skill_code", skill.skill_code)
            
            skill.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        """DELETE this skill"""
        skill = Skill.objects.get(pk=pk)
        skill.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
