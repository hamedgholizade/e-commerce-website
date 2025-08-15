from rest_framework import serializers

from locations.serializers import AddressSerializer
from stores.models import (
    Store,
    StoreItem
)


class StoreSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    
    class Meta:
        model = Store
        fields = [
            'id',
            'name',
            'description',
            'seller',
            'address'
        ]


class StoreItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = StoreItem
        fields = [
            'id',
            'price',
            'discount_price',
            'stock',
            'store',
            'product'
        ]
