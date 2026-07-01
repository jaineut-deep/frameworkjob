from rest_framework.permissions import BasePermission


class IsUserSelf(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsNotModerator(BasePermission):

    def has_permission(self, request, view):
        return not request.user.groups.filter(name="Moderators").exists()


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
