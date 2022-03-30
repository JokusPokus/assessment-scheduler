from django.db import models

from core.models import BaseModel


class Staff(BaseModel):
    """A member of the organization's staff involved in the execution of
    assessments.
    """

    organization = models.ForeignKey(
        'user.Organization',
        related_name='assessors',
        on_delete=models.CASCADE
    )
    email = models.EmailField(unique=True)
    assessment_phases = models.ManyToManyField(
        'schedule.AssessmentPhase',
        related_name='assessors'
    )

    class Meta:
        abstract = True


