from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)


class IsAdminOrSellerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            if not request.user.is_authenticated:
                return False 
            return bool(
                request.user.is_seller or
                request.user.is_staff or
                request.user.is_superuser
            )
        return True

