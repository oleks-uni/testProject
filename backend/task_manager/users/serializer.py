from rest_framework import serializers
from django.contrib.auth import authenticate 
from .models import UserModel
# from django.contrib.auth.password_validation import validate_password \\ do not use for now


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ('email', 'password', 'password2',)

    def validate_email(self, value):
        if UserModel.objects.filter(email=value) is None:
            if UserModel.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email has been already used")
        return value


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = UserModel.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
