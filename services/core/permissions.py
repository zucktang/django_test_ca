from rest_framework.permissions import (
    AllowAny,
    BasePermission,
)
from django.contrib.auth.models import AnonymousUser


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return request.user and not isinstance(request.user, AnonymousUser)
    
AllowAny=AllowAny