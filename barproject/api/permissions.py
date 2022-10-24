from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated


class AuthenticatedReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.method in SAFE_METHODS


class AnonCreateOrAdminRead(BasePermission):
    # customers(non-staff, anonymous) can only POST
    # staff can only GET
    def has_permission(self, request, view):
        if (
            request.user.is_authenticated and
            request.method in SAFE_METHODS
        ) or (
            not request.user.is_authenticated and
            request.method.upper() == "POST"
        ):
            return True

