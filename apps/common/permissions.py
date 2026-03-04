# Tenant Scoping nos Models: OrganizationScopedModel
from rest_framework.permissions import BasePermission

from apps.organizations.models import Membership, Organization


class HasActiveOrganization(BasePermission):
    """
    Permission tenant-scoped:
    - exige X-Organization-ID
    - garante que org existe
    - garante que usuário é membro ativo
    - seta request.organization
    """

    message = "Active organization required. Provide X-Organization-ID."

    def has_permission(self, request, view):
        org_id = getattr(request, "organization_id", None)
        if not org_id:
            return False

        if not request.user or not request.user.is_authenticated:
            return False

        try:
            org = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            # padrão de API: 404 para org inexistente
            # mas permission não consegue retornar 404 diretamente.
            # então devolvemos False e o RolePermission/HasActiveOrganization bloqueia.
            # (Se você quiser 404 mesmo, a gente trata em uma Exception custom depois.)
            return False

        is_member = Membership.objects.filter(
            user=request.user, organization=org, is_active=True
        ).exists()
        if not is_member:
            return False

        request.organization = org
        return True
