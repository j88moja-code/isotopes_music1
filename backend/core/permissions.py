from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user== request.user
class CustomUpdatePermission(permissions.BasePermission):
    """
    Permission class to check that a user can update his own resource only
    """

    def has_permission(self, request, view):
        # check that its an update request and user is modifying his resource only
        if view.action == 'update' and view.kwargs['pk']!=request.user.id:
            return False # not grant access
        return True # grant access otherwise