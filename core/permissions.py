from rest_framework.permissions import BasePermission


class IsAdminOrManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # admin can do anything, manager can only update and member can only read
        if request.method in ['PUT','PATCH']:
            return request.user.role in ['admin', 'manager']
        if request.method in ['POST', 'DELETE']:
            return request.user.role == 'admin'
        return True

