from rest_framework import serializers
from DsixRPGcompanionBE.models.skill_specialization import SkillSpecialization
        
class SkillSpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillSpecialization
        fields = ('specialization_name', 'specialization_code')