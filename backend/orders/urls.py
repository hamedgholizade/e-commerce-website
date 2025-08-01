from django.urls import path

from orders.views import (
    OrderListAPIView,
    OrderDetailAPIView,
    SellerOrderListAPIView,
    SellerOrderDetailAPIView,
)


urlpatterns = [
    path('order/', OrderListAPIView.as_view(), name='order-list'),
    path('order/<int:id>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('seller/', SellerOrderListAPIView.as_view(), name='seller-order-list'),
    path('seller/<int:id>/', SellerOrderDetailAPIView.as_view(), name='seller-order-detail'),
    
]

