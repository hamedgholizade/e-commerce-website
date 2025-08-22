from rest_framework import serializers

from products.models import ProductImage
from locations.models import Address
from stores.serializers import StoreItemSerializer
from carts.models import (
    Cart,
    CartItem
)


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    store = serializers.SerializerMethodField(read_only=True)
    store_item_data = StoreItemSerializer(read_only=True)
    unit_price = serializers.SerializerMethodField(read_only=True)
    total_discount = serializers.SerializerMethodField(read_only=True)
    total_item_price = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'quantity',
            'store',
            'cart',
            'store_item',
            'unit_price',
            'total_discount',
            'total_item_price',
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
    
    def get_product(self, obj):
        product = obj.store_item.product
        images = ProductImage.objects.filter(
            product=product.id, is_active=True
        )
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "images": [
                {
                    "id": image.id,
                    "image": image.image
                }
                for image in images
            ]
        }
    
    def get_store(self, obj):
        store = obj.store_item.store
        store_address = Address.objects.filter(
            store=store.id, is_active=True
        ).first()
        return store_address
    
    def get_unit_price(self, obj):
        return obj.unit_price
    
    def get_total_discount(self, obj):
        return obj.discount_price
    
    def get_total_item_price(self, obj):
        return obj.total_price
    
    def get_total_price(self, obj):
        return obj.cart.total_price
    
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
        return obj.total_price
        
    def get_total_discount(self, obj):
        return str(obj.total_discount)


class AddToCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(
        required=False, allow_null=True
    )
    
    def validate(self, attrs):
        if "quantity" not in attrs or attrs["quantity"] is None:
            attrs["quantity"] = 1
        return attrs

