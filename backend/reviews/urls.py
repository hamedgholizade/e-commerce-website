from rest_framework.routers import DefaultRouter

from reviews.views import ReviewModelViewSet

app_name='reviews'

router = DefaultRouter()
router.register('review', ReviewModelViewSet)
urlpatterns = []
urlpatterns += router.urls
