from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from base.permissions import IsOwnerObject
from carts.serializers import (
    CartItemSerializer,
    CartSerializer
)
from carts.models import (
    CartItem,
    Cart
)


class CartModelViewSet(ModelViewSet):
    queryset = Cart.objects.active()
    serializer_class = CartSerializer
    permission_classes = [IsOwnerObject]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).active()
    
    def perform_destroy(self, instance):
        instance.soft_delete()


class CartItemModelViewSet(ModelViewSet):
    queryset = CartItem.objects.active()
    serializer_class = CartItemSerializer
    permission_classes = [IsOwnerObject]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).active()
    
    def perform_destroy(self, instance):
        instance.soft_delete()
        