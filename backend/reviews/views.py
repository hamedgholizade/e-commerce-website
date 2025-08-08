from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters import rest_framework as dj_filters

from reviews.permissions import IsOwnerOrAdmin
from reviews.filters import ReviewFilter
from reviews.serializers import ReviewSerializer
from reviews.models import Review


class ReviewModelViewSet(ModelViewSet):
    queryset = Review.objects.active()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrAdmin]
    authentication_classes = [JWTAuthentication]
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_class = ReviewFilter
    
    def perform_destroy(self, instance):
        instance.soft_delete()
