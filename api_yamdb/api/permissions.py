from rest_framework import permissions


class IsAdminOrSuperuser(permissions.BasePermission):
    """ Доступ только для админов или суперюзеров. """

    def has_permission(self, request, view):

        return (
            request.user.is_superuser
            or request.user.is_staff
            or request.user.is_admin
            if request.user.is_authenticated else False
        )


class ISAdminOnlyEdit(permissions.BasePermission):
    """ Доступ только для админов или суперюзеров. """

    def has_permission(self, request, view):

        if request.method not in permissions.SAFE_METHODS:

            return (
                request.user.is_superuser
                or request.user.is_staff
                or request.user.is_admin
                if request.user.is_authenticated else False
            )

        else:
            return True


class ISAdminAuthorOrSuperuser(permissions.BasePermission):
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

            return (
                request.user == obj.author
                or request.user.is_superuser
                or request.user.is_admin
                or request.user.is_moderator
                if request.user.is_authenticated else False
            )

        else:
            return True
