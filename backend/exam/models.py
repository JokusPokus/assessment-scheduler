from django.db import models

from core.models import BaseModel


class Student(BaseModel):
    """A student who is to be assessed in a number of modules."""

    email = models.EmailField(unique=True)

    def __str__(self):
        return f'<Student: {self.email}>'
