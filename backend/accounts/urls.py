from django.urls import path
from rest_framework import routers

from accounts.views import AuthModelViewSet, RegisterAPIView


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='accounts-register')
]
