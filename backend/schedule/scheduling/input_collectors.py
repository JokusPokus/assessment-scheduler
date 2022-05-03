"""
Input collection to working memory for scheduling purposes
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.db.models import QuerySet

from schedule.models import Window, BlockSlot, BlockTemplate
from exam.models import Exam, Module, Student
from staff.models import Assessor, Helper


class BaseInputCollector(ABC):
    """Defines an interface for input collector classes."""

    @abstractmethod
    def collect(self) -> InputData:
        pass


@dataclass
class InputData:
    """Defines the input data requirements for
    any scheduling algorithm.
    """

    exams: QuerySet
    modules: QuerySet
    assessors: QuerySet
    helpers: QuerySet
    block_slots: QuerySet
    block_templates: QuerySet


class DBInputCollector(BaseInputCollector):
    """Collects input data from the database used by
    the Django project.
    """

    def __init__(self, window):
        self.window = window

    def collect(self) -> InputData:
        return InputData(
            exams=Exam.objects.filter(window=self.window),
            modules=Module.objects.filter(windows=self.window),
            assessors=Assessor.objects.filter(windows=self.window),
            helpers=Helper.objects.filter(windows=self.window),
            block_slots=BlockSlot.objects.filter(window=self.window),
            block_templates=BlockTemplate.objects.filter(windows=self.window)
        )
