from rest_framework.permissions import BasePermission


class IsUserSelf(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderators").exists()


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True

        return request.method in ("GET", "HEAD", "OPTIONS")
