# apps/crm_pipelines/serializers.py
from rest_framework import serializers

from apps.crm_pipelines.models import Pipeline, Stage


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = ["id", "name", "is_default", "ordering", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = [
            "id",
            "pipeline",
            "name",
            "order",
            "is_won",
            "is_lost",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_pipeline(self, pipeline: Pipeline) -> Pipeline:
        """
        Segurança: o pipeline informado deve pertencer à org ativa.
        Isso impede IDOR via pipeline UUID de outra org.
        """
        request = self.context.get("request")
        org = getattr(request, "organization", None)
        if not org:
            # A permission deve barrar antes,
            # mas mantemos defesa em profundidade.
            raise serializers.ValidationError("Active organization required.")

        if pipeline.organization_id != org.id:
            raise serializers.ValidationError(
                "Pipeline does not belong to the active organization."
            )
        return pipeline

    def validate(self, attrs):
        """
        Regra: não permitir won e lost simultaneamente.
        (Já existe no banco, mas validamos cedo para erro mais claro.)
        """
        is_won = attrs.get("is_won", getattr(self.instance, "is_won", False))
        is_lost = attrs.get("is_lost", getattr(self.instance, "is_lost", False))
        if is_won and is_lost:
            raise serializers.ValidationError("Stage cannot be both won and lost.")
        return attrs
