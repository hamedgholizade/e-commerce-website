from django.urls import path

from carts.views import (
    CartItemListAPIView,
    CartItemDetailAPIView,
    CartListAPIView,
    CartDetailAPIView
)

urlpatterns = [
    path('cart/', CartListAPIView.as_view(), name='cart-list'),
    path('cart/<int:id>/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('cart_item/', CartItemListAPIView.as_view(), name='cart-item-list'),
    path('cart_item/<int:id>/', CartItemDetailAPIView.as_view(), name='cart-item-detail'),
    
]
