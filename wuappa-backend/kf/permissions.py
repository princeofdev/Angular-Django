# -*- coding: utf-8 -*-
from rest_framework.permissions import BasePermission


class CustomActionPermissions(BasePermission):
    """
    A Permission class that allows to define different Django permissions to be checked for every type of action
    """
    list_permission = None
    retrieve_permission = None
    create_permission = None
    update_permission = None
    partial_update_permission = None
    destroy_permission = None

    def has_permission(self, request, view):
        if view.action == 'list' and self.list_permission is not None:
            return request.user.has_perm(self.list_permission)
        elif view.action == 'retrieve' and self.retrieve_permission is not None:
            return request.user.has_perm(self.retrieve_permission)
        elif view.action == 'create' and self.create_permission is not None:
            return request.user.has_perm(self.create_permission)
        elif view.action == 'update' and self.update_permission is not None:
            return request.user.has_perm(self.update_permission)
        elif view.action == 'partial_update' and self.partial_update_permission is not None:
            return request.user.has_perm(self.partial_update_permission)
        elif view.action == 'destroy' and self.destroy_permission is not None:
            return request.user.has_perm(self.destroy_permission)
        else:
            return True
