from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (
    RegisterAPIView,
    LoginAPIView
)


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='accounts-register'),
    path('login/', LoginAPIView.as_view(), name='login-token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    
]
