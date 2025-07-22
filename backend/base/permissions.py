from rest_framework.permissions import IsAuthenticated


class IsOwnerProfile(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj)


class IsOwnerObject(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user)
