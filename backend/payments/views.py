from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from payments.permissions import IsAuthenticatedAndReadOnly
from payments.serializers import PeymentSerializer
from payments.models import Payment


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.active()
    serializer_class = PeymentSerializer
    permission_classes = [IsAuthenticatedAndReadOnly]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        return self.queryset.filter(
            order__customer=self.request.user
            ).select_related('order')
