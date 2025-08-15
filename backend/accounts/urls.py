from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenRefreshView,
    TokenVerifyView
)

from accounts.views import (
    RegisterAPIView,
    LoginAPIView,
    OTPLoginAPIView,
    UserProfileAPIView
)

app_name='accounts'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login-token'),
    path('login/otp/', OTPLoginAPIView.as_view(), name='login-otp'),
    path('token/blacklist', TokenBlacklistView.as_view(), name='blacklist-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('token/verify/', TokenVerifyView.as_view(), name='verify-token'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    
]
