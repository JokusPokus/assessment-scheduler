from django.db import models
from django.core.exceptions import ValidationError
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
    """A coherent time span of assessments that may consist of various windows
    that can be scheduled separately.

    While windows are rather independent,
    various specifications are common to all windows of an assessment phase.
    """

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

    def __str__(self):
        return f"<{self.category.label} in {self.semester.label} {self.year}>"


class Window(BaseModel):
    """An independent time range that can be scheduled 'in one go'. One or more
    windows make up an assessment phase.

    Each window consists of one or more blocks, which in turn hosts a number
    of assessments and breaks.
    """

    assessment_phase = models.ForeignKey(
        'schedule.AssessmentPhase',
        related_name='windows',
        on_delete=models.CASCADE
    )
    start_date = models.DateField()
    end_date = models.DateField()
    block_length = models.IntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(420)]
    )

    def clean(self):
        super().clean()
        if start_date > end_date:
            raise ValidationError('Start date after end date')


class Block(BaseModel):
    """A collection of back-to-back exams and breaks of the same assessor.

    Each day within an assessment phase can contain a fixed number of blocks
    that have a fixed total length. Assessments within a block have a fixed,
    equal length. In turn, the length of assessments and breaks between
    different blocks may vary.

    E.g., the following 3-hour blocks are both feasible:

    +-----------------+      +-----------------+
    |   20 min exam   |      |   30 min exam   |
    |   20 min exam   |      |   30 min exam   |
    |   20 min exam   |      |   30 min exam   |
    |   20 min break  |      |   30 min break  |
    |   20 min exam   |      |   30 min exam   |
    |   20 min exam   |      |   30 min exam   |
    |   20 min break  |      +-----------------+
    |   20 min exam   |
    |   20 min exam   |
    +-----------------+
    """

    window = models.ForeignKey(
        'schedule.Window',
        related_name='blocks',
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
    exam_length = models.IntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(360)]
    )


class Slot(BaseModel):
    """An available time slot for an assessment."""

    block = models.ForeignKey(
        'schedule.Block',
        related_name='slots',
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
