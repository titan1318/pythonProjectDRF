<<<<<<< HEAD
from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        return request.user == view.get_object().owner
=======


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
>>>>>>> 189608c909cf437c2d8bfea0aafa445bf4172ede
