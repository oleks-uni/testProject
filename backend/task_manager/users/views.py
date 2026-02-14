from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import UserModel

from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import RegisterUserSerializer, LoginUserSerializer


class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User has been created successfully"}, status=201)
        return Response(serializer.errors, status=400)
    

class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=400)
        
        refresh_token = RefreshToken.for_user(user)

        return Response({
            'access': str(refresh_token.access_token),
            'refresh': str(refresh_token),
        })    


class LogoutUserView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'}, status=205)
        except Exception:
            return Response({'error': 'Invalid token'}, status=400)
        

class DeleteUserView(APIView):
    permission_classes = [permissions.IsAdminUser]


    def delete(self, request, id):
        try:
            user = UserModel.objects.get(id=id)
            user.delete()
            return Response({'message': 'User has been deleted successfully'}, status=200)
        except UserModel.DoesNotExist:
           return Response({'error': 'User not found'}, status=404) 
    
