from django.utils import timezone
from rest_framework import serializers
from DsixRPGcompanionBE.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'id', 'handle', 'bio', 'game_master', 'admin')

def get_current_date_formatted():
    """helper time/date stamp"""
    current_date = timezone.now().date()
    return current_date.strftime('%Y-%m-%d')