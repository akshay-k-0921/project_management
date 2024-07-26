from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'DELETE']:
            return request.user.role == 'admin'
        return True

class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['PUT','PATCH']:
            return request.user.role in ['admin', 'manager']
        if request.method in ['POST', 'DELETE']:
            return request.user.role == 'admin'
        return True

class IsMemberOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET' or request.user.role in ['admin', 'manager']
