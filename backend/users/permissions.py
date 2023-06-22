from rest_framework import permissions

from .serializers import UserSerializer


class ViewPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        data = UserSerializer(request.user).data

        view_access = any(p['name'] == 'view_' + view.permission_object for p in data['role']['permissions'])
        edit_access = any(p['name'] == 'edit_' + view.permission_object for p in data['role']['permissions'])

        if request.method == 'GET':
            return view_access or edit_access

        return edit_access

class hasSelfVotedOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.up_vote_by == request.user or obj.down_vote_by==request.user