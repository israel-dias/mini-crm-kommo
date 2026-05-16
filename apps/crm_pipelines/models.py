# apps/crm_pipelines/models.py
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q

from apps.common.tenant import OrganizationScopedModel


class Pipeline(OrganizationScopedModel):
    """
    Funil de vendas (ex.: "Vendas", "Renovação", etc.)
    Tenant-scoped: sempre pertence a uma Organization via OrganizationScopedModel.
    """

    name = models.CharField(max_length=120)
    # is_default: só 1 pipeline default por org (regra via constraint)
    is_default = models.BooleanField(default=False)

    # ordering: ordem de exibição dos pipelines dentro da org
    ordering = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            # Evita duplicar pipeline com mesmo nome na mesma org
            models.UniqueConstraint(
                fields=["organization", "name"],
                name="uq_pipeline_org_name",
            ),
            # Garante no máximo 1 pipeline default por org
            models.UniqueConstraint(
                fields=["organization"],
                condition=Q(is_default=True),
                name="uq_pipeline_one_default_per_org",
            ),
        ]
        indexes = [
            models.Index(fields=["organization", "ordering"], name="idx_pipeline_org_ordering"),
            models.Index(fields=["organization", "is_default"], name="idx_pipeline_org_default"),
        ]

    def __str__(self) -> str:
        return f"{self.name}"


class Stage(OrganizationScopedModel):
    """
    Etapa do pipeline (ex.: "Novo", "Contato", "Proposta", "Ganho", "Perdido").
    Tenant-scoped e pertencente a um Pipeline.
    """

    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name="stages")

    name = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)

    is_won = models.BooleanField(default=False)
    is_lost = models.BooleanField(default=False)

    conversion_probability = models.PositiveSmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        help_text="Probabilidade estimada de conversão desta etapa no funil, de 0 a 100.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "pipeline", "name"],
                name="uq_stage_org_pipeline_name",
            ),
            models.UniqueConstraint(
                fields=["organization", "pipeline", "order"],
                name="uq_stage_org_pipeline_order",
            ),
            models.CheckConstraint(
                condition=~(Q(is_won=True) & Q(is_lost=True)),
                name="ck_stage_not_won_and_lost",
            ),
        ]
        indexes = [
            models.Index(
                fields=["organization", "pipeline", "order"],
                name="idx_stage_org_pipeline_order",
            ),
            models.Index(fields=["organization", "pipeline"], name="idx_stage_org_pipeline"),
        ]

    def clean(self):
        """
        Garante consistência das regras de negócio da etapa do funil.
        """

        super().clean()

        if self.is_won and self.is_lost:
            raise ValidationError(
                "Uma etapa não pode ser marcada como ganha e perdida ao mesmo tempo."
            )

        if self.is_won and self.conversion_probability != 100:
            raise ValidationError(
                {"conversion_probability": ("Etapas ganhas devem ter probabilidade de 100%.")}
            )

        if self.is_lost and self.conversion_probability != 0:
            raise ValidationError(
                {"conversion_probability": ("Etapas perdidas devem ter probabilidade de 0%.")}
            )
