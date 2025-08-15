from rest_framework.routers import DefaultRouter

from stores.views import (
    StoreModelViewSet,
    StoreItemModelViewSet
)

app_name='stores'

router = DefaultRouter()
router.register('store', StoreModelViewSet)
router.register('store_item', StoreItemModelViewSet)

urlpatterns = [
    
]

urlpatterns += router.urls
