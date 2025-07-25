from rest_framework import serializers

from accounts.serializers import UserViewProfileSerializer
from carts.models import (
    Cart,
    CartItem
)


class CartSerializer(serializers.ModelSerializer):
    user = UserViewProfileSerializer(read_only=True)
    total_price = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'total_price']
        
        
class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
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
