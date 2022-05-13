from rest_framework.permissions import BasePermission
from rest_framework.request import Request


""" class IsBuyer(BasePermission):
    def has_permission(self, request: Request, _):
        restrict_methods = [
            "POST",
        ]

        if request.method in restrict_methods and (
            not request.user.is_anonymous
            and not request.user.is_admin
            and not request.user.is_seller
        ):
            return True
        return False """


class IsBuyerOrAdm(BasePermission):
    def has_permission(self, request: Request, _):

        if request.method == "POST" and (
            not request.user.is_anonymous
            and not request.user.is_admin
            and not request.user.is_seller
        ):
            return True

        if request.method == "GET" and (
            not request.user.is_anonymous
            and request.user.is_admin
            or request.user.is_seller
        ):
            return True

        return False
