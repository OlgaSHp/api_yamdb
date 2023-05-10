from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    pass


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    pass


class IsAdmin(permissions.BasePermission):
    pass
