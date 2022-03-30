from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

from core.models import BaseModel
from core.utils.datetime import current_year


MIN_BLOCK_LENGTH = 10
MAX_BLOCK_LENGTH = 420
MIN_EXAM_LENGTH = 10
MAX_EXAM_LENGTH = 360


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
    room_limit = models.PositiveIntegerField(null=True, blank=True)

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
        validators=[
            MinValueValidator(MIN_BLOCK_LENGTH),
            MaxValueValidator(MAX_BLOCK_LENGTH)
        ]
    )

    def clean(self):
        super().clean()
        if start_date > end_date:
            raise ValidationError('Start date after end date')


class BlockSlot(BaseModel):
    """An available slot for any number of blocks (constrained by personnel
    and room availabilities.
    """

    window = models.ForeignKey(
        'schedule.Window',
        related_name='block_slots',
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()


class Block(BaseModel):
    """A collection of concrete back-to-back exams and breaks
    of the same assessor.
    """

    block_slot = models.ForeignKey(
        'schedule.BlockSlot',
        related_name='blocks',
        on_delete=models.CASCADE
    )
    template = models.ForeignKey(
        'schedule.BlockTemplate',
        related_name='blocks',
        on_delete=models.CASCADE
    )


class BlockTemplate(BaseModel):
    """A specification of a block's precise structure, defining when each
    exam and break take place relative to the block's starting time.

    Assessments within a block have a fixed,
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

    windows = models.ManyToManyField(
        'schedule.Window',
        related_name='block_templates'
    )
    block_length = models.IntegerField(
        validators=[
            MinValueValidator(MIN_BLOCK_LENGTH),
            MaxValueValidator(MAX_BLOCK_LENGTH)
        ]
    )
    exam_length = models.IntegerField(
        validators=[
            MinValueValidator(MIN_EXAM_LENGTH),
            MaxValueValidator(MAX_EXAM_LENGTH)
        ]
    )
    exam_start_times = ArrayField(
        models.PositiveIntegerField()
    )

    def save(self, *args, **kwargs):
        if self.exam_start_times:
            self.exam_start_times.sort()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        self._enforce_exams_do_not_exceed_block()
        self._enforce_no_overlapping_exams()

    def _enforce_exams_do_not_exceed_block(self):
        if max(self.exam_start_times) + self.exam_length > block_length:
            raise ValidationError('Last exam starts too late')

    def _enforce_no_overlapping_exams(self):
        adjacent_exams = zip(self.exam_start_times, self.exam_start_times[1:])
        for earlier, later in adjacent_exams:
            if earlier + self.exam_length > later:
                raise ValidationError('Overlapping exams')


class ExamSlot(BaseModel):
    """An available time slot for an assessment."""

    block = models.ForeignKey(
        'schedule.Block',
        related_name='exam_slots',
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
