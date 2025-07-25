from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from stores.permissions import IsAdminOrSellerOrReadOnly
from stores.models import (
    Store,
    StoreItem
)
from stores.serializers import (
    StoreSerializer,
    StoreItemSerializer
)


class StoreModelViewSet(ModelViewSet):
    queryset = Store.objects.active()
    serializer_class = StoreSerializer
    permission_classes = [IsAdminOrSellerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_seller:
            return self.queryset.filter(seller=self.request.user)
        return self.queryset
    
    def perform_destroy(self, instance):
        instance.soft_delete()


class StoreItemModelViewSet(ModelViewSet):
    queryset = StoreItem.objects.active()
    serializer_class = StoreItemSerializer
    permission_classes = [IsAdminOrSellerOrReadOnly]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_seller:
            return self.queryset.filter(store__seller=self.request.user)
        return self.queryset
    
    def perform_destroy(self, instance):
        instance.soft_delete()
