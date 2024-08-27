from rest_framework import serializers
from DsixRPGcompanionBE.models.note import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'description', 'completed', 'temporary_field')
