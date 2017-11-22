from rest_framework.permissions import BasePermission

class IsAdminOrIsSelf(BasePermission):
    pass
    # def has_permission(self, request, view):


class IsPostOrIsAuthenticated(BasePermission):        

    def has_permission(self, request, view):
        # allow all POST requests
        if request.method == 'POST':
            return True

        # Otherwise, only allow authenticated requests
        return request.user and request.user.is_authenticated()
