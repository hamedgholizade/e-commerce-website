from rest_framework.routers import DefaultRouter

from locations.views import AddressModelViewSet

app_name='locations'

router = DefaultRouter()
router.register('address', AddressModelViewSet)

urlpatterns = [
    
]

urlpatterns += router.urls
