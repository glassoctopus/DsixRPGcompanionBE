from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from DsixRPGcompanionBE.models import User
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'id', 'handle', 'bio', 'game_master', 'admin')

def get_current_date_formatted():
    """helper time/date stamp"""
    current_date = timezone.now().date()
    return current_date.strftime('%Y-%m-%d')

class UserView(ViewSet):
    """User view for simple to-do list"""
    
    def retrieve(self, request, pk):
        """get a user"""
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, requests):
        """list all Users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        """POST / Create User """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            
            
            user = User.objects.create(
                uid=request.data["uid"],
                handle=request.data["handle"],
                bio=request.data["bio"],
                game_master=request.data["game_master"],
                admin=request.data["admin"],
            )
            
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        """PUT / Update a User"""
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, data = request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except user.DoesNotExist:
            raise Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        """DELETE"""
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            user.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)