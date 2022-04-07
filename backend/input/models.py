from django.db import models

from .processing import SheetProcessor
from core.models import BaseModel


class PlanningSheet(BaseModel):
    """A sheet that holds important information about an assessment phase,
    such as the exams to be scheduled and the respective students and
    assessors.
    """
    window = models.ForeignKey(
        'schedule.Window',
        related_name='planning_sheets',
        on_delete=models.CASCADE
    )
    csv = models.FileField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SheetProcessor(self.window, self.csv.path).populate_db()
