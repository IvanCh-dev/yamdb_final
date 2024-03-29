from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    '''Permissions IsAdmin .'''
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrReadOnly(BasePermission):
    '''Permissions IsAdminOrReadOnly.'''
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsModeratorOrAdminOrAuthor(BasePermission):
    '''Permissions IsModerator.'''
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator)
