from django.db import models
from django.contrib.auth.models import AbstractUser

from core.models import BaseModel


class User(AbstractUser):
    pass


class Organization(BaseModel):
    name = models.CharField(max_length=64)
