from django.db import transaction
from rest_framework import serializers

from stores.models import StoreItem
from stores.serializers import StoreItemSerializer
from carts.models import Cart
from orders.models import (
    OrderItem,
    Order
)


class OrderItemSerializer(serializers.ModelSerializer):
    store_item_data = StoreItemSerializer(read_only=True)
    get_price = serializers.CharField(read_only=True)
    get_total_price = serializers.CharField(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'order',
            'store_item',
            'price',
            'total_price',
            'is_active',
            'created_at',
            'updated_at',
            'get_price',
            'get_total_price',
            'store_item_data',
        ]
        read_only_fields = [
            'is_active',
            'created_at',
            'updated_at'
        ]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    get_total_price = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'address',
            'status',
            'total_price',
            'get_total_price',
            'is_active',
            'created_at',
            'updated_at',
            'items'
        ]
        
        read_only_fields = [
            'customer',
            'is_active',
            'created_at',
            'updated_at'
        ]

    def validate_address(self, value):
        user = self.context['request'].user
        address_id = value.id if hasattr(value, 'id') else value

        if not user.addresses.active().filter(id=address_id).exists():
            raise serializers.ValidationError('Wrong address selected')
        return value
    
    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        address = validated_data.pop('address')
        user_cart = Cart.objects.filter(user=user, is_active=True).first()
        if not user_cart:
            raise serializers.ValidationError('Your cart is empty')
        user_cart_items = user_cart.items.active()
        if not user_cart_items:
            raise serializers.ValidationError('Your cart is empty')
        
        locked_ids = [
            item.store_item_id for item in user_cart_items
        ]
        locked_items = {
            si.id: si for si in StoreItem.objects.select_for_update().filter(
                id__in=locked_ids
            )
        }
        total = user_cart.total_price
        order = Order.objects.create(
            customer=user,
            address=address,
            total_price=str(total),
            status=1
        )
        for item in user_cart_items:
            store_item = item.store_item
            if store_item.stock < item.quantity:
                raise serializers.ValidationError(
                    f"Not enough exist of {store_item.product.name}"
                    )
            store_item.stock -= item.quantity
            store_item.save(update_fields=["stock"])
            OrderItem.objects.create(
                order=order,
                store_item=item.store_item,
                quantity=item.quantity,
                price=str(item.unit_price),
                total_price=str(item.total_price)
            )
        for item in user_cart_items:
            item.soft_delete()
            
        return order
    
    def update(self, instance, validated_data):
        if 'status' not in validated_data or len(validated_data) > 1:
            raise serializers.ValidationError('Only can change status of order')
        instance.status = validated_data.get('status')
        instance.save()
        return instance
    