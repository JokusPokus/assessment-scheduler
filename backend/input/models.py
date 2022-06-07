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
        SheetProcessor(self.window, self.get_file_path()).populate_db()

    def get_file_path(self):
        """Get absolute path of the csv file."""
        if settings.APPLICATION_STAGE == 'development':
            return self.csv.path

        return self.csv.url
