from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    VerifyTokenAPIView
)


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='accounts-register'),
    path('login/', LoginAPIView.as_view(), name='login-token'),
    path('logout/', LogoutAPIView.as_view(), name='logout-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('token/verify/', VerifyTokenAPIView.as_view(), name='verify-token'),
    
]
