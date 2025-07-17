from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import (
    RegisterSerializer,
    LoginSerializer
)

User = get_user_model()

    
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.active()
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User registered successfully',
            'user': serializer.data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=201)
    
    
class LoginAPIView(generics.CreateAPIView):
    queryset = User.objects.active()
    serializer_class = LoginSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User logged in successfully',
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=200)
