from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from DsixRPGcompanionBE.models import Ability
from DsixRPGcompanionBE.serializers.ability import AbilitySerializer

class AbilityView(ViewSet):
    """Ability API endpoint for CRUD"""

    def create(self, request):
        """Create a new ability"""
        data = request.data
        
        if isinstance(data, list):
            created_abilities = []
            for ability in data:
                serializer = AbilitySerializer(data=ability)
                if serializer.is_valid():
                    ability = serializer.save()
                    created_abilities.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": f"{len(created_abilities)} abilities created.", "created_abilities": created_abilities}, status=status.HTTP_201_CREATED)
        else:
            serializer = AbilitySerializer(data=data)
            if serializer.is_valid():
                ability = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """Get a single ability by ID"""
        try:
            ability = Ability.objects.get(pk=pk)
            serializer = AbilitySerializer(ability)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ability.DoesNotExist:
            raise NotFound(detail="ability not found.", code=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """List all abilities"""
        abilities = Ability.objects.all()
        serializer = AbilitySerializer(abilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Update a ability"""
        try:
            ability = Ability.objects.get(pk=pk)
            serializer = AbilitySerializer(ability, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Ability.DoesNotExist:
            return Response({"error": "Ability not found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Delete a ability"""
        try:
            ability = Ability.objects.get(pk=pk)
            serializer = AbilitySerializer(ability)
            ability.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Ability.DoesNotExist:
            return Response({"error": "Ability not found."}, status=status.HTTP_404_NOT_FOUND)
