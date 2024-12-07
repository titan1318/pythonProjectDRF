from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """Проверка, является ли пользователь модератором."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """Проверка, является ли пользователь владельцем."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsUser(permissions.BasePermission):
    """Проверка, совпадает ли почта объекта, к которому осуществляется доступ, с почтой текущего пользователя."""

    def has_object_permission(self, request, view, obj):
        if obj.email == request.user.email:
            return True
        return False
