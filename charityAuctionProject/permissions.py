from rest_framework import permissions


class IsAuthorOrReadAndCreateOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit it. The model instance should have 'author' attribute
    """
    def has_object_permission(self, request, view, obj):
        # GET, HEAD or OPTIONS requests.
        if request.method in tuple(list(permissions.SAFE_METHODS) + ['POST']):
            return True

        if hasattr(obj, 'author'):
            return obj.author == request.user

        return False