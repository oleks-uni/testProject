import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from task_manager.auth import generate_jwt_token
from .models import UserModel


from .serializer import RegisterUserSerializer


class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User has been created successfully"}, status=201)
        return Response(serializer.errors, status=400)
    

class TokenObtainPair(APIView):
    def post (self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)

        if user:
            tokens = generate_jwt_token(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentails'}, status=status.HTTP_401_UNAUTHORIZED)
    

class TokenRefresh(APIView):
    def post (self, request):
        refresh_token = request.data.get('refresh_token')

        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = UserModel.objects.get(id=user_id)
            tokens = generate_jwt_token(user)
            return Response(tokens, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        except UserModel.DoesNotExist:
            return Response({'error': 'Invalid user'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutUserView(APIView):
    def post(self, request):
        return Response(
            {'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        

class DeleteUserView(APIView):
    permission_classes = [permissions.IsAdminUser]


    def delete(self, request, id):
        try:
            user = UserModel.objects.get(id=id)
            user.delete()
            return Response({'message': 'User has been deleted successfully'}, status=200)
        except UserModel.DoesNotExist:
           return Response({'error': 'User not found'}, status=404) 
