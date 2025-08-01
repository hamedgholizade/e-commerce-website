from rest_framework import generics, mixins
from rest_framework_simplejwt.authentication import JWTAuthentication

from orders.models import Order
from orders.serializers import OrderSerializer
from orders.utils import send_custom_email
from orders.permissions import (
    IsOrderOwner,
    IsSeller
)

class OrderListAPIView(generics.ListCreateAPIView):
    
    permission_classes = [IsOrderOwner]
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]   
    
    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user, is_active=True
            ).order_by('-created_at')


class OrderDetailAPIView(generics.RetrieveAPIView):
    
    permission_classes = [IsOrderOwner]
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]   
    
    
    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user, is_active=True
            ).order_by('-created_at')
    

class SellerOrderListAPIView(generics.ListAPIView):
    
    permission_classes = [IsSeller]
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            items__store_item__store__seller=user
            ).active().distinct().order_by('-created_at')
    

class SellerOrderDetailAPIView(generics.RetrieveUpdateAPIView):
    
    permission_classes = [IsSeller]
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            items__store_item__store__seller=user
            ).active().distinct().order_by('-created_at')
        
    def perform_update(self, serializer):
        instance = serializer.save()
        status_text = Order.ORDER_STATUS_CHOICES[instance.status]
        subject = 'Changing Order status'
        message = f'your order status is change to {status_text}'
        recipient = [instance.customer.email]
        send_custom_email(subject, message, recipient)
        