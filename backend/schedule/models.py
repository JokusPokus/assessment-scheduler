from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

from core.models import BaseModel
from core.utils.datetime import current_year


class Semester(models.TextChoices):
    SPRING = 'spring', 'Spring Semester'
    FALL = 'fall', 'Fall Semester'


class PhaseCategory(models.TextChoices):
    MAIN = 'main', 'Main Phase'
    REASSESSMENTS = 'reassessments', 'Re-Assessments'


class AssessmentPhase(BaseModel):
    organization = models.ForeignKey(
        'user.Organization',
        on_delete=models.CASCADE,
        related_name='phases'
    )
    year = models.IntegerField(
        default=current_year,
        validators=[MinValueValidator(2021)]
    )
    semester = models.CharField(
        max_length=32,
        choices=Semester.choices
    )
    category = models.CharField(
        max_length=32,
        choices=PhaseCategory.choices
    )
