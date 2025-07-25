from rest_framework.routers import DefaultRouter

from carts.views import (
    CartItemModelViewSet,
    CartModelViewSet
)

router = DefaultRouter()
router.register('cart', CartModelViewSet)
router.register('cart_item', CartItemModelViewSet)

urlpatterns = [
    
]

urlpatterns += router.urls
