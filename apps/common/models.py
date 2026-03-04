# Create your models here.
import uuid

from django.db import models


class TimeStampedModel(models.Model):
    """
    Modelo abstrato: adiciona created_at e updated_at automaticamente.
    Isso é padrão em sistemas profissionais para auditoria.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """
    Modelo abstrato: usa UUID como primary key.
    É mais seguro que integer (dificulta enumeração simples / scraping).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimeStampedModel):
    """
    Combina UUID + timestamps.
    Todo modelo importante do sistema herda isso.
    """

    class Meta:
        abstract = True
