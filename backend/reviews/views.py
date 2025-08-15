from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
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
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        user = self.request.user
        if not user.is_staff or not user.is_superuser:
            if serializer.instance.user.id != user.id:
                raise PermissionDenied("Can't update comment you aren't owner.")
        serializer.save()
    
    def perform_destroy(self, instance):
        user = self.request.user
        if not (user.is_staff or user.is_superuser or instance.user.id == user.id):
            raise PermissionDenied("Can't delete comment you aren't owner.")
        instance.soft_delete()
