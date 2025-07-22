import random
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from base.permissions import IsOwnerProfile
from accounts.utils import send_custom_email
from accounts.serializers import (
    RegisterSerializer,
    LoginSerializer,
    OTPLoginSerializer,
    UserViewProfileSerializer,
    UserUpdateProfileSerializer
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
        }, status=status.HTTP_201_CREATED)
    
    
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
        }, status=status.HTTP_200_OK)


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
        key = f"otp-sent:{mode}:{email_or_phone}"
            
        if otp_code:
            cached_code = cache.get(key)
            if cached_code != otp_code:
                return Response({
                    "error": "otp code is invalid or expired"
                }, status=400)
            refresh = RefreshToken.for_user(user)
            cache.delete(key)
            return Response({
                'message': 'User logged in successfully with OTP',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=200)
        
        if cache.get(key):
            return Response({
                "error": "Please wait before requesting another OTP."
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        code = str(random.randint(10000, 99999))
        cache.set(key, code, timeout=120)
        
        if mode == 'phone':
            return Response({
                "message": f"sending sms to {email_or_phone}",
                "otp": f"{code}"
            }, status=202)
        
        elif mode == 'email':
            subject = 'Your OTP Code'
            message = f'Your verification code is: {code}'
            recipient = [email_or_phone]
            send_custom_email(subject, message, recipient)
            return Response({
                "message": f"sending email to {email_or_phone}"
            }, status=202)    
    
    
class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.active()
    permission_classes = [IsOwnerProfile]
    authentication_classes = [JWTAuthentication]
    
    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UserUpdateProfileSerializer
        return UserViewProfileSerializer
    
    def get_object(self):
        return self.request.user   