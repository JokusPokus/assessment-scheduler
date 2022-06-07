from django.db import models
from django.conf import settings

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
    is_filled_out = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        attr_name = 'path' \
            if settings.APPLICATION_STAGE == 'development' \
            else 'url'

        SheetProcessor(self.window, getattr(self.csv, attr_name)).populate_db()
