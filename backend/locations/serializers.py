from rest_framework import serializers

from locations.models import Address


class AddressSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Address
        fields = '__all__'
        
        read_only_fields = [
            'is_active',
            'created_at',
            'updated_at'
        ]