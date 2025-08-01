from django.urls import path

from carts.views import (
    CartItemListAPIView,
    CartItemDetailAPIView,
    CartDetailAPIView
)

urlpatterns = [
    path('cart/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('items/', CartItemListAPIView.as_view(), name='cart-item-list'),
    path('items/<int:id>/', CartItemDetailAPIView.as_view(), name='cart-item-detail'),
    
]
