from rest_framework.permissions import BasePermission


class IsOwnerOrAdminOrModerator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
                request.user == obj.creator or
                request.user.is_staff or
                request.user.groups.filter(name="Модераторы").exists()
        )


class IsModeratorOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name="Модераторы").exists():
            return request.method in ["GET", "PATCH", "PUT"]
        return obj.owner == request.user


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_staff


class IsAdminOrModeratorEditOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        if request.method in ['PUT', 'PATCH'] and (
                request.user.is_superuser or
                request.user.groups.filter(name='Модераторы').exists()
        ):
            return True

        if request.method in ['POST', 'DELETE']:
            return False

        return False
