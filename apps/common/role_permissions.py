from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.organizations.models import Membership


class RolePermission(BasePermission):
    message = "You do not have permission to perform this action for this organization."

    def has_permission(self, request, view):
        org = getattr(request, "organization", None)
        if not org or not request.user or not request.user.is_authenticated:
            return False

        membership = (
            Membership.objects.filter(user=request.user, organization=org, is_active=True)
            .only("role")
            .first()
        )
        if not membership:
            return False

        if request.method in SAFE_METHODS:
            return True

        return membership.role in (Membership.Role.ADMIN, Membership.Role.MANAGER)
