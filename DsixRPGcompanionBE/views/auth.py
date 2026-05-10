from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

User = get_user_model()

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Both username and password required"}, status=400)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=401)

        login(request, user)

        return Response({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "bio": getattr(user, 'bio', ''),
                "game_master": getattr(user, 'game_master', False),
            }
        })

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)

        # Auto-login after registration (as requested)
        login(request, user)

        return Response({
            "message": "User created and logged in successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }
        }, status=201)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})

class SessionStatusAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                "isAuthenticated": True,
                "user": {
                    "id": request.user.id,
                    "username": request.user.username,
                    "email": request.user.email,
                    "bio": getattr(request.user, 'bio', ''),
                    "game_master": getattr(request.user, 'game_master', False),
                }
            })
        return Response({"isAuthenticated": False})

class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "bio": getattr(user, 'bio', ''),
            "game_master": getattr(user, 'game_master', False),
        })

    def patch(self, request):
        user = request.user
        if 'bio' in request.data:
            user.bio = request.data['bio']
        if 'game_master' in request.data:
            user.game_master = request.data['game_master']
        user.save()
        return Response({"message": "User updated successfully"})