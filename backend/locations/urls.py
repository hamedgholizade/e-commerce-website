from rest_framework.routers import DefaultRouter

from locations.views import AddressModelViewSet

router = DefaultRouter()
router.register('address', AddressModelViewSet)

urlpatterns = [
    
]

urlpatterns += router.urls
