from rest_framework import permissions


class AdminOrSuperuser(permissions.BasePermission):
    """ Доступ только для админов или суперюзеров. """

    def has_permission(self, request, view):

        if request.user.is_authenticated:
            return (
                request.user.is_superuser
                or request.user.role == 'admin'
            )
        else:
            return False


class AdminOnlyCanEdit(permissions.BasePermission):
    """ Доступ только для админов или суперюзеров. """

    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            if request.user.is_authenticated:
                return (
                    request.user.is_superuser
                    or request.user.role == 'admin'
                )
            else:
                return False
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            if request.user.is_authenticated:
                return (
                    request.user.is_superuser
                    or request.user.role == 'admin'
                )
            else:
                return False
        else:
            return True


class GetAll_PostAuth_ElseAdminAuthorSuper(permissions.BasePermission):
    """
    Get - все пользователи
    Post - все авторизованные
    Все оставшиеся - только административный персонал и автор.
    """

    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return (request.user.is_authenticated)
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            if request.user.is_authenticated:
                return (
                    request.user == obj.author
                    or request.user.is_superuser
                    or request.user.role == 'admin'
                    or request.user.role == 'moderator'
                )
            return False
        else:
            return True
