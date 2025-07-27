from rest_framework import serializers

from accounts.serializers import UserViewProfileSerializer
from carts.models import (
    Cart,
    CartItem
)


class CartItemSerializer(serializers.ModelSerializer):
    unit_price = serializers.FloatField(read_only=True)
    total_price = serializers.FloatField(read_only=True)
    
    class Meta:
        model = CartItem
        fields = [
            'id',
            'cart',
            'store_item',
            'quantity',
            'unit_price',
            'total_price'
            ]
        
        
class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_price', 'items']
        