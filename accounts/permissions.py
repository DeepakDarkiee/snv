from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission


class IsLogin(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        else:
            raise ErrorStatus()


class ErrorStatus(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {"error": True, "message": "Please Login First"}
    default_code = "not_authenticated"
