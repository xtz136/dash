from rest_framework.permissions import BasePermission


class IsAdminOrIsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return self.request.user == obj


class IsPostOrIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        # allow all POST requests
        if request.method == 'POST':
            return True

        # Otherwise, only allow authenticated requests
        return request.user and request.user.is_authenticated()
