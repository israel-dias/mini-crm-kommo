# apps/crm_pipelines/views.py
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import HasActiveOrganization
from apps.common.role_permissions import RolePermission
from apps.common.viewsets import TenantModelViewSet
from apps.crm_pipelines.models import Pipeline, Stage
from apps.crm_pipelines.serializers import PipelineSerializer, StageSerializer


class PipelineViewSet(TenantModelViewSet):
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer
    permission_classes = [IsAuthenticated, HasActiveOrganization, RolePermission]
    filterset_fields = ["is_default"]
    search_fields = ["name"]
    ordering_fields = ["ordering", "name", "created_at"]
    ordering = ["ordering", "name"]


class StageViewSet(TenantModelViewSet):
    queryset = Stage.objects.select_related("pipeline").all()
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticated, HasActiveOrganization, RolePermission]
    filterset_fields = ["pipeline", "is_won", "is_lost"]
    search_fields = ["name"]
    ordering_fields = ["order", "name", "created_at"]
    ordering = ["order", "name"]
