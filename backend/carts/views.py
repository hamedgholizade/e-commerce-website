from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from base.permissions import IsOwnerObject
from carts.permissions import IsOwnerOfCartItem
from carts.serializers import (
    CartItemSerializer,
    CartSerializer
)
from carts.models import (
    CartItem,
    Cart
)

class CartDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsOwnerObject]
    authentication_classes = [JWTAuthentication]
    
    def get_object(self):
        obj, _ = Cart.objects.get_or_create(user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_destroy(self, instance):
        instance.soft_delete()
        instance.items.active().soft_delete()
    

class CartItemListAPIView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsOwnerOfCartItem]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).active()
    
    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(
            user = self.request.user
        )
        serializer.save(cart=cart)
        
        
class CartItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsOwnerOfCartItem]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).active()

    def perform_destroy(self, instance):
        instance.soft_delete()
        