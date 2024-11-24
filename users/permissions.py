

from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Модераторы').exists()

class IsAdminOrModeratorEditOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH']:
            return request.user.is_authenticated and (
                request.user.is_staff or request.user.groups.filter(name='Модераторы').exists()
            )
        return request.method in ['GET']
