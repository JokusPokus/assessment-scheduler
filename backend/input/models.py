from django.db import models

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


class SheetRecord(BaseModel):
    """Holds the information of one record - i.e., row - in a particular
    planning sheet.
    """
    planning_sheet = models.ForeignKey(
        'input.PlanningSheet',
        related_name='records',
        on_delete=models.CASCADE
    )

    assessmentId = models.CharField(max_length=32)
    student = models.CharField(max_length=64)
    semester = models.CharField(max_length=16)
    shortCode = models.CharField(max_length=16)
    module = models.CharField(max_length=64)
    grade = models.CharField(max_length=16, null=True, blank=True)
    assessor = models.CharField(max_length=64)
    assistant = models.CharField(max_length=64, null=True, blank=True)
    startTime = models.DateTimeField(null=True, blank=True)
    endTime = models.DateTimeField(null=True, blank=True)
    assessmentStatus = models.CharField(max_length=16, null=True, blank=True)
    assessmentStyle = models.CharField(max_length=16)
    proposalText = models.TextField(null=True, blank=True)
    assessmentType = models.CharField(max_length=16)
    examinationForms = models.CharField(max_length=16, null=True, blank=True)
    learningUnit = models.CharField(max_length=64, null=True, blank=True)
    proposalStatus = models.CharField(max_length=16, null=True, blank=True)
    createdAt = models.DateTimeField(null=True, blank=True)
    updatedAt = models.DateTimeField(null=True, blank=True)
