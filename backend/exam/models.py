from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.models import BaseModel
from schedule.models import MIN_EXAM_LENGTH, MAX_EXAM_LENGTH


DEFAULT_EXAM_LENGTH = 20


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
        default=DEFAULT_EXAM_LENGTH,
        validators=[
            MinValueValidator(MIN_EXAM_LENGTH),
            MaxValueValidator(MAX_EXAM_LENGTH)
        ]
    )
    alternative_length = models.IntegerField(
        default=DEFAULT_EXAM_LENGTH,
        validators=[
            MinValueValidator(MIN_EXAM_LENGTH),
            MaxValueValidator(MAX_EXAM_LENGTH)
        ]
    )
    windows = models.ManyToManyField(
        'schedule.Window',
        related_name='modules'
    )

    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.code


class ExamStyle(models.TextChoices):
    STANDARD = 'standard', 'Standard'
    ALTERNATIVE = 'alternative', 'Alternative'


class Exam(BaseModel):
    """A concrete module assessment taken by a student."""

    code = models.CharField(max_length=64)
    window = models.ForeignKey(
        'schedule.Window',
        related_name='exams',
        on_delete=models.CASCADE
    )
    module = models.ForeignKey(
        'exam.Module',
        related_name='exams',
        on_delete=models.CASCADE
    )
    style = models.CharField(
        max_length=32,
        choices=ExamStyle.choices
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
