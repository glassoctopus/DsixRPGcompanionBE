from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from DsixRPGcompanionBE.models import Archetype

# TODO
# class ArchetypeEquipmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ArchetypeEquipment
#         fields = ('id', 'archetype', 'equipment', 'quantity')

class ArchetypeSerializer(serializers.ModelSerializer):
    # archetype_equipment = ArchetypeEquipmentSerializer(many=True, required=False)

    class Meta:
        model = Archetype
        fields = ('id', 'archetype_name', 'archetype_personality', 'archetype_background', 'archetype_objectives', 'archetype_a_quote', 'archetype_force_sensitive', 'archetype_dexiterity', 'archetype_knowledge', 'archetype_mechanical', 'archetype_perception', 'archetype_strength', 'archetype_technical', 'archetype_force_control', 'archetype_force_sense', 'archetype_force_alter')
        
    def create(self, validated_data):
        # equipment_list = validated_data.pop('archetype_equipment', [])
        archetype = Archetype.objects.create(**validated_data)
        # for piece in equipment_list:
        #     ArchetypeEquipment.objects.create(archetype=archetype, **piece)
        return archetype

class ArchetypeView(ViewSet):
    """Archetype API endpoint for CRUD"""
    def create(self, request, *args, **kwargs):
        data = request.data
        print("Received create request with data:", data)        
        if isinstance(data, list):
            created_archetypes = []
            for item in data:
                serializer = ArchetypeSerializer(data=item)
                if serializer.is_valid():
                    archetype = serializer.save()
                    created_archetypes.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(created_archetypes, status=status.HTTP_201_CREATED)
        else:
            serializer = ArchetypeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk):
        """Retrieve a single Archetype"""
        try:
            archetype = Archetype.objects.get(pk=pk)
            serializer = ArchetypeSerializer(archetype)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Archetype.DoesNotExist:
            raise NotFound(detail="Archetype not found.", code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """List all Archetypes"""
        archetypes = Archetype.objects.all()
        serializer = ArchetypeSerializer(archetypes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        """Update an Archetype"""
        try:
            archetype = Archetype.objects.get(pk=pk)
            serializer = ArchetypeSerializer(archetype, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Archetype.DoesNotExist:
            return Response({"error": "Archtype not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        """Delete an Archetype"""
        archetype = Archetype.objects.get(pk=pk)
        archetype.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
