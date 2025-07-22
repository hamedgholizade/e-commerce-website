from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from base.permissions import IsOwnerObject
from locations.models import Address
from locations.serializers import AddressSerializer

class AddressModelViewSet(ModelViewSet):
    queryset = Address.objects.active()
    serializer_class = AddressSerializer
    permission_classes = [IsOwnerObject]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user).active()
    
    def perform_destroy(self, instance):
        instance.soft_delete()
        