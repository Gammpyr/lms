from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        is_moderator = request.user.groups.filter(name='Moderator').exists()
        return request.user.is_authenticated and is_moderator

        # if request.method in ['POST', 'DELETE'] and is_moderator:
        #     return False
        #
        # if request.user.is_authenticated:
        #     return is_moderator
        #
        # return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.owner == request.user
        return False