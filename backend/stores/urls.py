from rest_framework.routers import DefaultRouter

from stores.views import (
    StoreModelViewSet,
    StoreItemModelViewSet
)

router = DefaultRouter()
router.register('store', StoreModelViewSet)
router.register('store_item', StoreItemModelViewSet)

urlpatterns = [
    
]

urlpatterns += router.urls
