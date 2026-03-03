from django.db import models

# Create your models here.
# apps/accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    User customizado (mínimo).
    Você pode adicionar campos depois (ex: phone).
    """
    email = models.EmailField(unique=True)

    # opcional: tornar email o username principal no futuro
    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return self.username