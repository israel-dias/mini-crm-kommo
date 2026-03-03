from rest_framework.routers import DefaultRouter

from apps.crm_pipelines.views import PipelineViewSet, StageViewSet

router = DefaultRouter()
router.register(r"pipelines", PipelineViewSet, basename="pipeline")
router.register(r"stages", StageViewSet, basename="stage")

urlpatterns = router.urls