from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.models import Post


class PostPermission(BasePermission):
    def has_object_permission(self, request, view, obj: Post):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
