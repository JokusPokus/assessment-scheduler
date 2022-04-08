from django.db import models

from core.models import BaseModel


class Staff(BaseModel):
    """A member of the organization's staff involved in the execution of
    assessments.
    """

    organization = models.ForeignKey(
        'user.Organization',
        related_name='%(class)s',
        on_delete=models.CASCADE
    )
    email = models.EmailField(unique=True)
    assessment_phases = models.ManyToManyField(
        'schedule.AssessmentPhase',
        related_name='%(class)s'
    )
    available_blocks = models.ManyToManyField(
        'schedule.BlockSlot',
        related_name='%(class)s'
    )

    class Meta:
        abstract = True


class Assessor(Staff):
    """A module assessor."""

    def __str__(self):
        return self.email


class Helper(Staff):
    """An assistant to the module assessors."""

    def __str__(self):
        return self.email
