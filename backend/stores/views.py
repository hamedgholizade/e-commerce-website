from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied

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
    
    def perform_create(self, serializer):
        seller = serializer.validated_data['seller']
        if seller != self.request.user.id:
            raise PermissionDenied("Can't create store you don't own")
        serializer.save()
        
    def perform_update(self, serializer):
        seller = serializer.validated_data.get('seller', serializer.instance.seller)
        if seller != self.request.user.id:
            raise PermissionDenied("Can't update store you don't own.")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.seller != self.request.user:
            raise PermissionDenied("Can't delete store you don't own.")
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
    
    def perform_create(self, serializer):
        store = serializer.validated_data['store']
        user = self.request.user
        if store.seller != user:
            raise PermissionDenied("Can't create item of a store you don't own")
        serializer.save()
        
    def perform_update(self, serializer):
        store = serializer.validated_data.get('store', serializer.instance.store)
        if store.seller != self.request.user:
            raise PermissionDenied("Can't update item of a store you don't own.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.store.seller != self.request.user:
            raise PermissionDenied("Can't delete item of a store you don't own.")
        instance.soft_delete()
