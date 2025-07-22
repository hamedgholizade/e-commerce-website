from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from products.permissions import IsAdminOrSellerOrReadOnly
from products.models.category_model import Category
from products.models.product_image_model import ProductImage
from products.models.product_model import Product
from products.serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductImageSerializer
)


class ProductImageModelViewSet(ModelViewSet):
    queryset = ProductImage.objects.active()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrSellerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_destroy(self, instance):
        instance.soft_delete()
    

class ProductModelViewSet(ModelViewSet):
    queryset = Product.objects.active()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrSellerOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_destroy(self, instance):
        instance.soft_delete()
        

class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.active()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrSellerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
    def perform_destroy(self, instance):
        instance.soft_delete()

    @action(methods=['GET'], detail=True)
    def ancestors(self, request, pk=None):
        category = self.get_object()
        ancestors = self._get_ancestors(category=category)
        serializer = self.get_serializer(ancestors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def _get_ancestors(self, category):
        result = []
        current = category.parent
        while current:
            result.insert(0, current)
            current = current.parent
        return result


    @action(methods=['GET'], detail=True)
    def descendants(self, request, pk=None):
        root = self.get_object()
        descendants = self._get_descendants(root=root)
        serializer = self.get_serializer(descendants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def _get_descendants(self, root):
        result = []
        def recurse(node):
            for child in node.subcategories.all():
                result.append(child)
                recurse(child)
        recurse(root)
        return result
