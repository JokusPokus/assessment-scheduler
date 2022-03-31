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

    def __str__(self):
        return f"<User: {self.email}>"


class Organization(BaseModel):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"<Organization: {self.name}>"


def code_university_id() -> int:
    return Organization.objects.get_or_create(name='CODE University')[0].id
