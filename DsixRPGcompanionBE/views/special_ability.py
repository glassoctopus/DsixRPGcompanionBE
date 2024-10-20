from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from DsixRPGcompanionBE.models import SpecialAbility
from DsixRPGcompanionBE.serializers.special_ability import SpecialAbilitySerializer

class SpecialAbilityView(ViewSet):
    """Special Ability API endpoint for CRUD"""

    def create(self, request):
        """Create a new special ability"""
        data = request.data
        
        if isinstance(data, list):
            created_abilities = []
            for ability in data:
                serializer = SpecialAbilitySerializer(data=ability)
                if serializer.is_valid():
                    ability = serializer.save()
                    created_abilities.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": f"{len(created_abilities)} abilities created.", "created_abilities": created_abilities}, status=status.HTTP_201_CREATED)
        else:
            serializer = SpecialAbilitySerializer(data=data)
            if serializer.is_valid():
                ability = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """Get a single special ability by ID"""
        try:
            ability = SpecialAbility.objects.get(pk=pk)
            serializer = SpecialAbilitySerializer(ability)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SpecialAbility.DoesNotExist:
            raise NotFound(detail="Special ability not found.", code=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """List all special abilities"""
        abilities = SpecialAbility.objects.all()
        serializer = SpecialAbilitySerializer(abilities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Update a special ability"""
        try:
            ability = SpecialAbility.objects.get(pk=pk)
            serializer = SpecialAbilitySerializer(ability, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SpecialAbility.DoesNotExist:
            return Response({"error": "Special ability not found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Delete a special ability"""
        try:
            ability = SpecialAbility.objects.get(pk=pk)
            serializer = SpecialAbilitySerializer(ability)
            ability.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SpecialAbility.DoesNotExist:
            return Response({"error": "Special ability not found."}, status=status.HTTP_404_NOT_FOUND)
