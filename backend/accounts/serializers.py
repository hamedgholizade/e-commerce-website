from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'phone',
            'email',
            'password',
            'first_name',
            'last_name',
            'is_seller',
            'picture'
            ]

    def create(self, validated_data):
        phone = validated_data.get("phone")
        validated_data['username'] = phone
        return super().create(validated_data)
    

class LoginSerializer(serializers.Serializer):
    phone_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs['phone_or_email'],
            password=attrs['password']
        )
        if not user:
            raise serializers.ValidationError(
                "No active account found with the given credentials"
                )
        attrs['user'] = user
        return attrs
