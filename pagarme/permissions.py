from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class IsAdmim(BasePermission):
    def has_permission(self, request: Request, _):
        restrict_methods = [
            "GET",
        ]

        if request.method in restrict_methods and (
            request.user.is_anonymous or not request.user.is_admin
        ):
            return False
        return True


class IsBuyer(BasePermission):
    def has_permission(self, request: Request, _):
        restrict_methods = [
            "GET",
            "POST",
        ]

        if request.method in restrict_methods and (
            not request.user.is_anonymous
            and not request.user.is_admin
            and not request.user.is_seller
        ):
            return True
        return False


class IsSeller(BasePermission):
    def has_permission(self, request: Request, _):
        restrict_methods = ["POST", "PATCH"]

        if request.method in restrict_methods and (
            request.user.is_anonymous or not request.user.is_seller
        ):
            return False
        return True
