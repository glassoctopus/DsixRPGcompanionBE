from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from DsixRPGcompanionBE.models import User
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('uid', 'id', 'bio', 'game_master', 'admin')

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

    def create(self, request):
        """POST / Create User """
        user = User.objects.create(
            bio=request.data["bio"],
            uid=request.data["uid"],
        )
        
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """PUT / Update a User"""
        try:
            user = User.objects.get(pk=pk)
            data = request.data
            
            # Debug: print request data
            print("Request data:", data)
            
            # update if in request data
            user.bio = data.get("bio")
            
            user.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk):
        """DELETE"""
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        