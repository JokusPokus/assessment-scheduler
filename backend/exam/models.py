from django.db import models

from core.models import BaseModel


class Student(BaseModel):
    """A student who is to be assessed in a number of modules."""

    email = models.EmailField(unique=True)

    def __str__(self):
        return f'<Student: {self.email}>'


class Module(BaseModel):
    """An academic unit that requires assessments."""

    code = models.CharField(max_length=32)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'<Module: {self.name}>'
