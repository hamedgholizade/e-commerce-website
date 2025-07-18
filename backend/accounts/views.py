import random
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import (
    RegisterSerializer,
    LoginSerializer,
    OTPLoginSerializer
)

User = get_user_model()

    
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.active()
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User logged in successfully',
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=200)


class OTPLoginAPIView(generics.CreateAPIView):
    queryset = User.objects.active()
    serializer_class = OTPLoginSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        otp_code = serializer.validated_data.get('otp_code')
        email_or_phone = serializer.validated_data['email_or_phone']
        
        mode = serializer.validated_data['mode']
        user = serializer.validated_data['user']
        if not user:
            return Response({
                "error": "Invalid phone number or email address"
            }, status=400)
        key = f"otp:{mode}:{email_or_phone}"
        
        if otp_code:
            cached_code = cache.get(key)
            if cached_code != otp_code:
                return Response({
                    "error": "otp code is invalid or expired"
                }, status=400)
            cache.delete(key)
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User logged in successfully with OTP',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=200)

        code = str(random.randint(10000, 99999))
        cache.set(key, code, timeout=120)
        
        if mode == 'phone':
            return Response({
                "message": f"sending sms to {email_or_phone}"
            }, status=202)
        
        elif mode == 'email':
            return Response({
                "message": f"sending email to {email_or_phone}"
            }, status=202)    
            