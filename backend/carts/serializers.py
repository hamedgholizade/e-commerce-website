from rest_framework import serializers

from stores.serializers import StoreItemSerializer
from carts.models import (
    Cart,
    CartItem
)


class CartItemSerializer(serializers.ModelSerializer):
    store_item_data = StoreItemSerializer(read_only=True)
    unit_price = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = CartItem
        fields = [
            'id',
            'cart',
            'store_item',
            'quantity',
            'unit_price',
            'total_price',
            'store_item_data',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'cart',
            'is_active',
            'created_at',
            'updated_at'
        ]
    
    def get_unit_price(self, obj):
        return str(obj.unit_price)
    
    def get_total_price(self, obj):
        return str(obj.total_price)
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "Quantity must be at least 1."
            )
        return value
    
    def validate(self, attrs):
        store_item = attrs.get("store_item")
        quantity = attrs.get("quantity", 1)
        if store_item and hasattr(store_item, "stock"):
            if quantity > store_item.stock:
                raise serializers.ValidationError(
                    "Quantity exceeds available stock"
                )
        return attrs
        
    def create(self, validated_data):
        user = self.context['request'].user
        store_item = validated_data.pop('store_item')
        quantity = validated_data.pop('quantity')
        cart, _ = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, store_item=store_item, is_active=True
        )
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return cart_item  
    
    
class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(read_only=True)
    total_discount = serializers.SerializerMethodField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'total_price',
            'total_discount',
            'is_active',
            'created_at',
            'updated_at',
            'items'
        ]
        read_only_fields = [
            'is_active',
            'created_at',
            'updated_at'
        ]
        
    def get_total_price(self, obj):
        return str(obj.total_price)
        
    def get_total_discount(self, obj):
        return str(obj.total_discount)
    