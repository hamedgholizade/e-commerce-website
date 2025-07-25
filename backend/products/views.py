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
    ProductImageSerializer,
    SellerProductSerializer
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
    permission_classes = [IsAdminOrSellerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_seller:
            return SellerProductSerializer
        return ProductSerializer

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
    def parents(self, request, pk=None):
        category = self.get_object()
        parents = self._get_parents(category=category)
        serializer = self.get_serializer(parents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def _get_parents(self, category):
        result = []
        current = category.parent
        while current:
            result.insert(0, current)
            current = current.parent
        return result


    @action(methods=['GET'], detail=True)
    def children(self, request, pk=None):
        category = self.get_object()
        children = self._get_children(category=category)
        serializer = self.get_serializer(children, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def _get_children(self, category):
        result = []
        def recurse(node):
            for child in node.subcategories.all():
                result.append(child)
                recurse(child)
        recurse(category)
        return result
