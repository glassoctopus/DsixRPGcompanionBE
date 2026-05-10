from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from DsixRPGcompanionBE.models import Archetype
from DsixRPGcompanionBE.serializers.archetype import ArchetypeSerializer
from DsixRPGcompanionBE.audit.services import AuditService
from DsixRPGcompanionBE.audit.middleware import AuditContext
from DsixRPGcompanionBE.models.audit_log import AuditLog
   
class ArchetypeViewSet(ViewSet):
    """Archetype viewset, CRUD"""
    def create(self, request, *args, **kwargs):
        data = request.data       
        print("Received create request with data:", data)
        source_override = AuditContext.get_source_type(request)
        
        if isinstance(data, list):
            created_archetypes = []
            payload_override = AuditLog.SingleOrBulk.BULK_ENTRIES_ACTION
            for item in data:
                serializer = ArchetypeSerializer(data=item)
                if serializer.is_valid():
                    archetype = serializer.save()
                    created_archetypes.append(serializer.data)
                    AuditService.log(
                        action='CREATE',
                        content_object=archetype,
                        request=request,
                        old_data=None,
                        new_data=serializer.data,
                        override_source_type=source_override,
                        override_payload_type=payload_override
                    )
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": f"There were {len(created_archetypes)} entries...", "created archetypes": created_archetypes}, status=status.HTTP_201_CREATED)
        else:
            payload_override = AuditLog.SingleOrBulk.SINGLE_ENTRY_ACTION
            serializer = ArchetypeSerializer(data=data)
            if serializer.is_valid():
                archetype = serializer.save()
                AuditService.log(
                    action='CREATE',
                    content_object=archetype,
                    request=request,
                    old_data=None,
                    new_data=serializer.data,
                    override_source_type=source_override,
                    override_payload_type=payload_override
                )
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
        """Update one or more Archetypes"""
        data = request.data
        source_override = AuditContext.get_source_type(request)
        payload_override = AuditLog.SingleOrBulk.BULK_ENTRIES_ACTION
        if isinstance(data, list):
            results = []
            for item in data:
                if 'id' not in item:
                    return Response({"error": "Each item must have an id field"}, status=status.HTTP_400_BAD_REQUEST)
                
                try:
                    archetype = Archetype.objects.get(pk=item['id'])
                    old_serializer = ArchetypeSerializer(archetype)
                    old_data = old_serializer.data
                    serializer = ArchetypeSerializer(archetype, data=item, partial=True)
                    if serializer.is_valid():
                        updated_archetype = serializer.save()
                        AuditService.log(
                            action='UPDATE',
                            content_object=updated_archetype,
                            request=request,
                            old_data=old_data,
                            new_data=serializer.data,
                            override_source_type=source_override,
                            override_payload_type=payload_override
                        )
                        results.append(serializer.data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Archetype.DoesNotExist:
                    return Response({"error": f"Archetype with id {item['id']} not found"}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:  # Add this
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"updated": results}, status=status.HTTP_200_OK)
        
        else:
            try:
                archetype = Archetype.objects.get(pk=pk)
                old_serializer = ArchetypeSerializer(archetype)
                old_data = old_serializer.data
                payload_override = AuditLog.SingleOrBulk.SINGLE_ENTRY_ACTION
                serializer = ArchetypeSerializer(archetype, data=data, partial=True)
                if serializer.is_valid():
                    updated_archetype = serializer.save()
                    AuditService.log(
                        action='UPDATE',
                        content_object=updated_archetype,
                        request=request,
                        old_data=old_data,
                        new_data=serializer.data,
                        override_source_type=source_override,
                        override_payload_type=payload_override
                    )
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Archetype.DoesNotExist:
                return Response({"error": "Archetype not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        """Delete one or more Archetypes"""
        data = request.data
        source_override = AuditContext.get_source_type(request)
        payload_override = AuditLog.SingleOrBulk.BULK_ENTRIES_ACTION
        if isinstance(data, list):
            deleted_ids = []
            for item_id in data:
                try:
                    archetype = Archetype.objects.get(pk=item_id)
                    serializer = ArchetypeSerializer(archetype)
                    old_data = serializer.data
                    
                    AuditService.log(
                        action='DELETE',
                        content_object=archetype,
                        request=request,
                        old_data=old_data,
                        new_data=None,
                        override_source_type=source_override,
                        override_payload_type=payload_override
                    )
                    archetype.delete()
                    deleted_ids.append(item_id)
                except Archetype.DoesNotExist:
                    return Response({"error": f"Archetype with id {item_id} not found"}, status=status.HTTP_404_NOT_FOUND)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"deleted": deleted_ids}, status=status.HTTP_204_NO_CONTENT)
        
        else:
            # Single delete
            try:
                archetype = Archetype.objects.get(pk=pk)
                serializer = ArchetypeSerializer(archetype)
                old_data = serializer.data
                payload_override = AuditLog.SingleOrBulk.SINGLE_ENTRY_ACTION
                AuditService.log(
                    action='DELETE',
                    content_object=archetype,
                    request=request,
                    old_data=old_data,
                    new_data=None,
                    override_source_type=source_override,
                    override_payload_type=payload_override
                )
                archetype.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Archetype.DoesNotExist:
                return Response({"error": "Archetype not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)