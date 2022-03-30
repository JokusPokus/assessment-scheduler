from django.db import models

from core.models import BaseModel


class Student(BaseModel):
    """A student who is to be assessed in a number of modules."""

    organization = models.ForeignKey(
        'user.Organization',
        related_name='students',
        on_delete=models.CASCADE
    )
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'<Student: {self.email}>'


class Module(BaseModel):
    """An academic unit taken by students and requiring assessments."""

    organization = models.ForeignKey(
        'user.Organization',
        related_name='modules',
        on_delete=models.CASCADE
    )
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'<Module: {self.name}>'


class Exam(BaseModel):
    """A concrete module assessment taken by a student."""

    code = models.CharField(max_length=64)
    module = models.ForeignKey(
        'exam.Module',
        related_name='exams',
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        'exam.Student',
        related_name='exams',
        on_delete=models.CASCADE
    )
    assessor = models.ForeignKey(
        'staff.Assessor',
        related_name='exams',
        on_delete=models.CASCADE,
    )
    helper = models.ForeignKey(
        'staff.Helper',
        related_name='exams',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    time_slot = models.OneToOneField(
        'schedule.ExamSlot',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
