from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import CustomAuthToken
router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', CustomAuthToken.as_view())
]