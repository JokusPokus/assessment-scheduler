"""
Input collection to working memory for scheduling purposes
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, TypedDict, List

from django.db.models import QuerySet

from schedule.models import Window, BlockSlot, BlockTemplate
from exam.models import Exam, Module, Student, ExamStyle
from staff.models import Assessor, Helper


SlotId = int
Email = int


class AvailInfo(TypedDict):
    """Data about the number and email ids of helpers available
    in a given block slot.
    """
    count: int
    helpers: List[Email]


class Workload(TypedDict):
    exam_length: int
    count: int


HelperAvails = Dict[SlotId, AvailInfo]
AssessorWorkloads = Dict[Email, Workload]


@dataclass
class InputData:
    """Defines the input data requirements for
    any scheduling algorithm.
    """

    exams: QuerySet
    modules: QuerySet
    assessors: QuerySet
    assessor_workload: AssessorWorkloads
    helpers: QuerySet
    helper_avails: HelperAvails
    block_slots: QuerySet
    block_templates: QuerySet


class BaseInputCollector(ABC):
    """Defines an interface for input collector classes."""

    @abstractmethod
    def collect(self) -> InputData:
        pass


class DBInputCollector(BaseInputCollector):
    """Collects input data from the database used by
    the Django project.
    """

    def __init__(self, window):
        self.window = window
        self.exams = Exam.objects.filter(window=window)
        self.modules = Module.objects.filter(windows=window)
        self.assessors = Assessor.objects.filter(windows=window)
        self.helpers = Helper.objects.filter(windows=window)
        self.block_slots = BlockSlot.objects.filter(window=window)
        self.block_templates = BlockTemplate.objects.filter(windows=self.window)

    def collect(self) -> InputData:
        return InputData(
            exams=self.exams,
            modules=self.modules,
            assessors=self.assessors,
            assessor_workload=self._assessor_workload,
            helpers=self.helpers,
            helper_avails=self._helper_avails,
            block_slots=self.block_slots,
            block_templates=self.block_templates,
        )

    @property
    def _helper_avails(self):
        return {
            slot.id: {
                'count': slot.helper.count(),
                'helpers': slot.helper.all()
            }
            for slot in self.block_slots
        }

    @property
    def _exam_lengths(self) -> set:
        return {template.exam_length for template in self.block_templates}

    @property
    def _assessor_workload(self) -> AssessorWorkloads:
        def get_workload(assessor: Assessor) -> Workload:
            exams = self.exams.filter(assessor=assessor)
            workload = {}
            for length in self._exam_lengths:
                standard_count = exams.filter(
                    style=ExamStyle.STANDARD,
                    module__standard_length=length
                ).count()
                alt_count = exams.filter(
                    style=ExamStyle.ALTERNATIVE,
                    module__alternative_length=length
                ).count()
                workload[length] = standard_count + alt_count
            return workload

        return {
            assessor.email: get_workload(assessor)
            for assessor in self.assessors
        }

