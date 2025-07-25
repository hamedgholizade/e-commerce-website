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
            'children'
        ]
    
    def create(self, validated_data):
        if not validated_data.get('image'):
            validated_data.pop('image', None)
        return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    best_price = serializers.SerializerMethodField()
    best_seller = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'stock',
            'rating',
            'best_price',
            'best_seller',
            'is_active',
            'created_at',
            'updated_at',
            'images',
            'category'
        ]
        read_only_fields = ['is_active', 'created_at', 'updated_at']

    def get_best_price(self, obj):
        items = obj.store_items.active()
        prices = []
        for item in items:
            prices.append(
                item.discount_price if item.discount_price 
                else item.price
                )
        return min(prices) if prices else None
    
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


class SellerProductSerializer(ProductSerializer):
    
    def create(self, validated_data):
        validated_data['is_active'] = False
        return super().create(validated_data)
