# Create your models here.
# apps/organizations/models.py
from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class Organization(BaseModel):
    """
    Tenant = Empresa/Organização.
    Tudo no sistema vai pertencer a uma Organization.
    """

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)

    def __str__(self) -> str:
        return self.name


class Membership(BaseModel):
    """
    Liga User <-> Organization e define papel (RBAC).
    Ex: admin, manager, sales, viewer
    """

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        MANAGER = "manager", "Manager"
        SALES = "sales", "Sales"
        VIEWER = "viewer", "Viewer"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships"
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.SALES)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "organization")  # impede membership duplicado

    def __str__(self) -> str:
        return f"{self.user} @ {self.organization} ({self.role})"
