from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Review
from stores.models import Store
from products.models import Product

User = get_user_model()


class ReviewUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'phone',
            'email',
            'first_name',
            'last_name'
        ]
        read_only_fields = [
            'phone',
            'email',
            'first_name',
            'last_name'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), required=False, allow_null=True
    )
    store = serializers.PrimaryKeyRelatedField(
        queryset=Store.objects.all(), required=False, allow_null=True
    )
    user_data = ReviewUserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'product',
            'store',
            'parent',
            'comment',
            'user_data',
            'is_active',
            'updated_at',
            'created_at'
        ]
        read_only_fields = [
            'user',
            'is_active',
            'updated_at',
            'created_at'
        ]

    def validate(self, attrs):
        request = self.context['request']
        product = attrs.get('product')
        store = attrs.get('store')

        if request.method == 'POST':
            if not product and not store:
                raise serializers.ValidationError(
                    "Comment must be related to either a product or a store."
                    )
            if product and Review.objects.filter(
                user=request.user, product=product, is_active=True
                ).exists():
                    raise serializers.ValidationError(
                        "You already submitted a comment for this product."
                    )
            if store and Review.objects.filter(
                user=request.user, store=store, is_active=True
                ).exists():
                    raise serializers.ValidationError(
                        "You already submitted a comment for this store."
                    )
        return attrs
    
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
    