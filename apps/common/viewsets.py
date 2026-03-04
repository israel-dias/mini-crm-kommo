# Tenant Scoping nas Queries (ViewSet base)
from rest_framework import viewsets
from rest_framework.exceptions import NotFound


class TenantModelViewSet(viewsets.ModelViewSet):
    """
    Base para qualquer endpoint multi-tenant.
    - get_queryset filtra pela org ativa
    - perform_create força organization=org ativa
    """

    def get_organization(self):
        org = getattr(self.request, "organization", None)
        if not org:
            # 404 aqui não é obrigatório, mas mantém padronizado
            raise NotFound("Active organization not provided. Use X-Organization-ID header.")
        return org

    def get_queryset(self):
        qs = super().get_queryset()
        org = self.get_organization()
        return qs.filter(organization=org)

    def perform_create(self, serializer):
        org = self.get_organization()
        serializer.save(organization=org)
