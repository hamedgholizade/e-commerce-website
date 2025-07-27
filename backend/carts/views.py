from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
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


class CartListAPIView(GenericAPIView):
    serializer_class = CartSerializer
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).active()
    
    def get(self, request):
        carts = self.get_queryset()
        serializer = self.get_serializer(carts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user != self.request.user.id:
            raise PermissionDenied("Can't create cart you don't own")
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartDetailAPIView(GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsOwnerObject]
    authentication_classes = [JWTAuthentication]
    
    def get_object(self, id):
        obj = get_object_or_404(Cart, id=id)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request, id):
        serializer = self.get_serializer(instance=self.get_object(id))
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        serializer = self.get_serializer(
            instance=self.get_object(id), data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        serializer = self.get_serializer(
            instance=self.get_object(id), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        cart = self.get_object(id)
        cart.soft_delete()
        return Response({"deleted": True}, status=status.HTTP_204_NO_CONTENT)
    

class CartItemListAPIView(GenericAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsOwnerOfCartItem]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).active()
    
    def get(self, request):
        car_items = self.get_queryset()
        serializer = self.get_serializer(car_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        cart = Cart.objects.filter(user=request.user).active().first()
        if not cart:
            return Response(
                {"detail": "Active cart not found."}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_data = serializer.validated_data['cart']
        if cart_data != cart.id:
            raise PermissionDenied("Can't create cart-item you don't own")
        serializer.save(cart=cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemDetailAPIView(GenericAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsOwnerOfCartItem]
    authentication_classes = [JWTAuthentication]
    
    def get_object(self, id):
        obj =get_object_or_404(CartItem, id=id)
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get(self, request, id):
        serializer = self.get_serializer(instance=self.get_object(id))
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        serializer = self.get_serializer(
            instance=self.get_object(id), data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        serializer = self.get_serializer(
            instance=self.get_object(id), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        cart_item = self.get_object(id)
        cart_item.soft_delete()
        return Response({"deleted": True}, status=status.HTTP_204_NO_CONTENT)
        