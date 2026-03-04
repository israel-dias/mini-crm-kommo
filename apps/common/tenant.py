# apps/common/tenant.py
from django.db import models

from apps.common.models import BaseModel
from apps.organizations.models import Organization


class OrganizationScopedModel(BaseModel):
    """
    Todo modelo do CRM deve herdar isso.
    Garante que existe organization_id no dado.
    """

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="%(class)s_items"
    )

    class Meta:
        abstract = True
