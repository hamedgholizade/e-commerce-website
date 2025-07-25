from rest_framework import serializers

from products.serializers import ProductSerializer
from accounts.serializers import UserViewProfileSerializer
from locations.serializers import AddressSerializer
from stores.models import (
    Store,
    StoreItem
)


class StoreSerializer(serializers.ModelSerializer):
    address  = AddressSerializer(read_only=True) 
    seller = UserViewProfileSerializer(read_only=True)
    
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
    store = StoreSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    
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
