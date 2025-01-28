from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.exceptions import NotFound
from DsixRPGcompanionBE.models import Species
from DsixRPGcompanionBE.serializers.species import SpeciesSerializer

class SpeciesView(ViewSet):
    """Species API endpoint for CRUD"""

    def create(self, request):
        """Create a new species"""
        data = request.data
        
        if isinstance(data, list):
            created_species = []
            for species in data:
                serializer = SpeciesSerializer(data=species)
                if serializer.is_valid():
                    species = serializer.save()
                    created_species.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": f"{len(created_species)} species created.", "created_species": created_species}, status=status.HTTP_201_CREATED)
        else:
            serializer = SpeciesSerializer(data=data)
            if serializer.is_valid():
                species = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """Get a single species by ID"""
        try:
            species = Species.objects.get(pk=pk)
            serializer = SpeciesSerializer(species)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Species.DoesNotExist:
            raise NotFound(detail="Species not found.", code=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """List all species"""
        species = Species.objects.all()
        serializer = SpeciesSerializer(species, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """Update a species"""
        try:
            species = Species.objects.get(pk=pk)
            serializer = SpeciesSerializer(species, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Species.DoesNotExist:
            return Response({"error": "Species not found."}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk):
        """Delete a species"""
        try:
            species = Species.objects.get(pk=pk)
            serializer = SpeciesSerializer(species)
            species.delete()
            return Response({"deleted": f"Species {serializer.data} was successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        except Species.DoesNotExist:
            return Response({"error": "Species not found."}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'], url_path='by_name')
    def by_name(self, request):
        """Retrieve a species by its name"""
        species_name = request.query_params.get('name', None)
        # print(f"Received query parameter 'name': {species_name}")
        if not species_name:
            return Response({"error": "Name parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            species = Species.objects.get(species_name=species_name)
            serializer = SpeciesSerializer(species)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Species.DoesNotExist:
            raise NotFound(detail="Species not found.", code=status.HTTP_404_NOT_FOUND)
