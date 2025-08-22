from decimal import Decimal, InvalidOperation
from rest_framework import serializers
from django.db.models import Sum

from products.models.category_model import Category
from products.models.product_image_model import ProductImage
from products.models.product_model import Product
from orders.models import OrderItem
from stores.models import StoreItem


class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductImage
        fields = '__all__'
        read_only_fields = [
            'is_active',
            'created_at',
            'updated_at'
        ]
        

class RecursiveCategorySerializer(serializers.Serializer):
    
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(
            instance, context=self.context
        )
        return serializer.data
    
    
class CategorySerializer(serializers.ModelSerializer):
    children = RecursiveCategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'description',
            'image',
            'parent',
            'children',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'is_active',
            'created_at',
            'updated_at'
        ]
    
    def create(self, validated_data):
        if not validated_data.get('image'):
            validated_data.pop('image', None)
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    best_price = serializers.SerializerMethodField(read_only=True)
    best_seller = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'stock',
            'rating',
            'category',
            'images',
            'best_price',
            'best_seller',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'stock',
            'is_active',
            'created_at',
            'updated_at'
        ]

    def get_best_price(self, obj):
        items = obj.store_items.active()
        prices = []
        for item in items:
            item_price = item.discount_price or item.price
            try:
                prices.append(Decimal(item_price))
            except (InvalidOperation, TypeError):
                continue
        return str(min(prices)) if prices else None
    
    def get_best_seller(self, obj):
        best = (
            OrderItem.objects.filter(
                store_item__product=obj
                ).values(
                    'store_item__store'
                ).annotate(
                    total_sold=Sum('quantity')
                ).order_by('-total_sold')
            ).first()
        if best:
            store_id = best['store_item__store']
            store_item = StoreItem.objects.filter(
                product=obj, store=store_id
            ).active().first()
            if store_item:
                return {
                    "store_id": store_item.store.id,
                    "store_name": store_item.store.name,
                    "product_id": store_item.product.id,
                    "product_name": store_item.product.name,
                    "price": store_item.price,
                    "discount_price": store_item.discount_price
                }
        return None


class SellerProductSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        allow_empty=True,
        write_only=True
    )
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'category',
            'images',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'created_at',
            'updated_at'
        ]
    
    def create(self, validated_data):
        validated_data['is_active'] = False
        product =  super().create(validated_data)
        images = validated_data.get('images', [])
        if images:
            for image in images:
                ProductImage.objects.create(
                    product=product, image=image
                )
        return product
        
