from django.urls import path

from payments.views import PaymentListAPIView

app_name='payments'


urlpatterns = [
    path('payment/', PaymentListAPIView.as_view(), name='payment-list')
]
