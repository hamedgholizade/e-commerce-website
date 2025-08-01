from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated
)


class IsOrderOwner(IsAuthenticated):
    
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user
    

class IsSeller(BasePermission):
    
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, 'is_seller', False)
        )
