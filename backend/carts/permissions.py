from rest_framework.permissions import IsAuthenticated


class IsOwnerOfCartItem(IsAuthenticated):
    
    def has_object_permission(self, request, view, obj):
        return obj.cart.user == request.user
