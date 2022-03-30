from django.db import models

from core.models import BaseModel


class PlanningSheet(BaseModel):
    """A sheet that holds important information about an assessment phase,
    such as the exams to be scheduled and the respective students and
    assessors.
    """
    assessment_phase = models.ForeignKey(
        'schedule.AssessmentPhase',
        related_name='planning_sheets',
        on_delete=models.CASCADE
    )
    csv = models.FileField()
