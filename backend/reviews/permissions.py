from rest_framework.permissions import IsAuthenticated


class IsOwnerOrAdmin(IsAuthenticated):
    
    def has_object_permission(self, request, view, obj):
        if request.method in ('PATCH', 'PUT', 'DELETE'):
            return obj.user == request.user or request.user.is_staff
        return True
