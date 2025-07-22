from rest_framework.routers import DefaultRouter

from products.views import(
    ProductImageModelViewSet,
    ProductModelViewSet,
    CategoryModelViewSet
)

router = DefaultRouter()
router.register('product', ProductModelViewSet)
router.register('image', ProductImageModelViewSet)
router.register('category', CategoryModelViewSet)

urlpatterns = []

urlpatterns += router.urls
