from django.db import models

from core.models import BaseModel


class Assessor(BaseModel):
    """A module assessor."""

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

    def __str__(self):
        return f'<Assessor: {self.email}>'
