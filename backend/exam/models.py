from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.models import BaseModel
from schedule.models import MIN_EXAM_LENGTH, MAX_EXAM_LENGTH


class Student(BaseModel):
    """A student who is to be assessed in a number of modules."""

    organization = models.ForeignKey(
        'user.Organization',
        related_name='students',
        on_delete=models.CASCADE
    )
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Module(BaseModel):
    """An academic unit taken by students and requiring assessments."""

    organization = models.ForeignKey(
        'user.Organization',
        related_name='modules',
        on_delete=models.CASCADE
    )
    code = models.CharField(max_length=32)
    name = models.CharField(max_length=64)
    standard_length = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(MIN_EXAM_LENGTH),
            MaxValueValidator(MAX_EXAM_LENGTH)
        ]
    )
    alternative_length = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(MIN_EXAM_LENGTH),
            MaxValueValidator(MAX_EXAM_LENGTH)
        ]
    )

    def __str__(self):
        return self.code


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

    def __str__(self):
        return f"<{self.module.code}: {self.student.email}>"
