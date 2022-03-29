from django.db import models
from django.contrib.auth.models import AbstractUser

from core.models import BaseModel


class User(AbstractUser):
    organization = models.ForeignKey(
        'user.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


class Organization(BaseModel):
    name = models.CharField(max_length=64)
