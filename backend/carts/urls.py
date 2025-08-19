from django.urls import path

from carts.views import (
    CartItemListAPIView,
    CartItemDetailAPIView,
    CartDetailAPIView,
    AddToCartAPIView
)

app_name='carts'

urlpatterns = [
    path('cart/', CartDetailAPIView.as_view(), name='cart-detail'),
    path('items/', CartItemListAPIView.as_view(), name='cart-item-list'),
    path('items/<int:pk>/', CartItemDetailAPIView.as_view(), name='cart-item-detail'),
    path('add_to_cart/<int:pk>/', AddToCartAPIView.as_view(), name='add-to-cart')
    
]
