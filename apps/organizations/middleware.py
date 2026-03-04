# apps/organizations/middleware.py
from django.utils.deprecation import MiddlewareMixin


class ActiveOrganizationMiddleware(MiddlewareMixin):
    """
    Middleware mínimo:
    - lê X-Organization-ID
    - guarda em request.organization_id (string/uuid)
    A validação (existência e membership) fica para as permissions no DRF.
    """

    HEADER_NAME = "HTTP_X_ORGANIZATION_ID"

    def process_request(self, request):
        request.organization = None
        request.organization_id = request.META.get(self.HEADER_NAME)
