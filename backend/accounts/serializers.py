from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts.utils import get_or_create_user
from locations.serializers import AddressSerializer
from accounts.utils import (
    custom_normalize_email,
    custom_normalize_phone,
    custom_validate_email,
    custom_validate_phone
)

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, min_length=8
    )

    class Meta:
        model = User
        fields = [
            'phone',
            'email',
            'password',
            'first_name',
            'last_name'
            ]
        
    def validate_phone(self, value):
        value = custom_normalize_phone(value)
        if value:
            return value
        raise serializers.ValidationError(
                "Invalid phone number"
            )
    
    def validate_email(self, value):
        value = custom_normalize_email(value)
        if value:
            return value
        raise serializers.ValidationError(
                "Invalid email address"
            )
        
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance


class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(
        write_only=True, max_length=128, min_length=8,style={'input_type': 'password'}
    )
    
    def validate_email_or_phone(self, value):
        normalized_phone = custom_normalize_phone(value)
        normalized_email = custom_normalize_email(value)
        if normalized_phone:
            return normalized_phone
        elif normalized_email:
            return normalized_email
        else:
            raise serializers.ValidationError(
                "Invalid phone number or email address"
            )

    def validate(self, attrs):
        user = authenticate(
            username=attrs['email_or_phone'],
            password=attrs['password']
        )
        if not user:
            raise serializers.ValidationError(
                "No active account found with the given credentials"
                )
        attrs['user'] = user
        return attrs
    

class OTPLoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(max_length=100, required=True)
    otp_code = serializers.CharField(
        max_length=16, required=False, allow_blank=True
    )

    def validate_email_or_phone(self, value):
        normalized_phone = custom_normalize_phone(value)
        normalized_email = custom_normalize_email(value)
        if normalized_phone:
            return normalized_phone
        elif normalized_email:
            return normalized_email
        else:
            raise serializers.ValidationError(
                "Invalid phone number or email address"
            )
    
    def validate(self, attrs):
        email_or_phone = attrs.get('email_or_phone')

        if custom_validate_phone(email_or_phone):
            attrs['mode'] = 'phone'
            user, _ = get_or_create_user(phone=email_or_phone, is_active=True)
        elif custom_validate_email(email_or_phone):
            attrs['mode'] = 'email'
            user = User.objects.filter(email=email_or_phone).first()
        if not user:    
            raise serializers.ValidationError(
                "No active account found with the given credential"
            )
        attrs['user'] = user
        return attrs


class UserViewProfileSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    picture = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = User
        exclude = ['password']
    
        read_only_fields = [
            'is_seller',
            'is_active',
            'created_at',
            'updated_at'
        ]
    
    
class UserUpdateProfileSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    picture = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = [
            'phone',
            'email',
            'first_name',
            'last_name',
            'password',
            'picture',
            'addresses'
        ]        
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        picture = validated_data.pop('picture', None)
        if picture is not None:
            instance.picture = picture
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save(update_fields=['password'])
        return instance
    