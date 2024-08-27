from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from DsixRPGcompanionBE.models.note import Note
from DsixRPGcompanionBE.serializers.note import NoteSerializer

class NoteView(ViewSet):
    def retrieve(self, request, pk):
        try:
            note = Note.objects.get(pk=pk)
            serializer = NoteSerializer(note, context={'request': request})
            return Response(serializer.data)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        note = Note.objects.create(
            title=request.data['title'],
            description=request.data['description'],
            completed=request.data['completed'],
            temporary_field=request.data['temporary_field']
        )
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        try:
            note = Note.objects.get(pk=pk)
            note.title = request.data['title']
            note.description = request.data['description']
            note.completed = request.data['completed']
            note.temporary_field = request.data['temporary_field']
            note.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        try:
            note = Note.objects.get(pk=pk)
            note.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Note.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)