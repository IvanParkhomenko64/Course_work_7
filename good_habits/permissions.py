from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Кастомный класс для возможности доступа только пользователю к привычкам"""

    def has_object_permission(self, request, view, obj):
        if request.user.pk == obj.user.pk:
            return True
        else:
            return False


class IsPublic(permissions.BasePermission):
    """Кастомный класс для возможности доступа только к активным привычкам"""

    def has_object_permission(self, request, view, obj):
        if request.user.pk == obj.user.pk or obj.is_public is True:
            return True
        else:
            return False