from django.urls import path

from payments.views import PaymentListAPIView


urlpatterns = [
    path('payment/', PaymentListAPIView.as_view())
]
