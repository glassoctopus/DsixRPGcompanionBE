from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from DsixRPGcompanionBE.models import User
from DsixRPGcompanionBE.serializers.user import UserSerializer
from ..permissions import IsAdminOrReadOnly
from django.contrib.contenttypes.models import ContentType
from DsixRPGcompanionBE.models import AuditLog

class UserViewSet(ViewSet):
    """User view for simple to-do list"""
    permission_classes = [IsAdminOrReadOnly] 
    
    def retrieve(self, request, pk):
        """get a user"""
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """list all Users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """POST / Create User"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # password hashing is handled inside serializer
            AuditLog.objects.create(
                content_type=ContentType.objects.get_for_model(user),
                object_id=user.pk,
                action=AuditLog.ActionType.CREATE,
                source_type=AuditLog.SourceOfEntry.USER,
                payload_type=AuditLog.SingleOrBulk.SINGLE_ENTRY_ACTION,
                user=request.user,
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """PUT / Update a User"""
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                updated_user = serializer.save()
                AuditLog.objects.create(
                    content_type=ContentType.objects.get_for_model(updated_user),
                    object_id=updated_user.pk,
                    action=AuditLog.ActionType.UPDATE,
                    source_type=AuditLog.SourceOfEntry.USER,
                    payload_type=AuditLog.SingleOrBulk.SINGLE_ENTRY_ACTION,
                    user=request.user,
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        """DELETE"""
        try:
            user = User.objects.get(pk=pk)
            AuditLog.objects.create(
                content_type=ContentType.objects.get_for_model(user),
                object_id=user.pk,
                action=AuditLog.ActionType.DELETE,
                source_type=AuditLog.SourceOfEntry.USER,
                payload_type=AuditLog.SingleOrBulk.SINGLE_ENTRY_ACTION,
                user=request.user,
                old_data=UserSerializer(user).data,  # snapshot
            )
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  # deleted, no content
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)