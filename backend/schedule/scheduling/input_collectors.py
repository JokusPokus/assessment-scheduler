"""
Input collection to working memory for scheduling purposes
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
import math
from typing import Dict, TypedDict, List

from django.db.models import QuerySet

from schedule.models import Window, BlockSlot, BlockTemplate
from exam.models import Exam, Module, Student, ExamStyle
from staff.models import Assessor, Helper


SlotId = int
Email = int
ExamLength = int
Count = int
BlockCount = Dict[ExamLength, Count]
AssessorBlockCounts = Dict[Email, BlockCount]


class AvailInfo(TypedDict):
    """Data about the number and email ids of helpers available
    in a given block slot.
    """
    count: int
    helpers: List[Email]


HelperAvails = Dict[SlotId, AvailInfo]


@dataclass
class InputData:
    """Defines the input data requirements for
    any scheduling algorithm.
    """

    exams: QuerySet
    modules: QuerySet
    assessors: QuerySet
    assessor_workload: AssessorBlockCounts
    helpers: QuerySet
    helper_avails: HelperAvails
    block_slots: QuerySet
    block_templates: QuerySet


class BaseInputCollector(ABC):
    """Defines an interface for input collector classes."""

    @abstractmethod
    def collect(self) -> InputData:
        pass


class WorkloadCalculator:
    """Calculates the assessors' workloads in terms of exams and
    blocks.
    """

    def __init__(self, exams, assessors, block_templates):
        self.exams = exams
        self.assessors = assessors
        self.block_templates = block_templates

    @property
    def assessor_block_counts(self) -> AssessorBlockCounts:
        """Calculate the number of blocks each assessor has to execute
        if exams are assigned as efficiently as possible.

        Return the result as a dictionary.
        """
        workload = self._assessor_exam_counts
        for length in self._exam_lengths:
            template = self.block_templates.get(exam_length=length)
            exams_per_block = len(template.exam_start_times)

            for assessor in workload:
                workload[assessor][length] = math.ceil(
                    workload[assessor][length] / exams_per_block
                )

        return workload

    @property
    def _assessor_exam_counts(self):
        """Calculate the number of exams each assessor has to execute
        and return the result as a dictionary.
        """
        def get_workload(assessor: Assessor) -> Dict[Email, Dict]:
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

    @property
    def _exam_lengths(self) -> set:
        return {template.exam_length for template in self.block_templates}


class DBInputCollector(BaseInputCollector):
    """Collects input data from the database used by
    the Django project.
    """

    def __init__(self, window, workload_calculator=None):
        self.window = window
        self.exams = Exam.objects.filter(window=window)
        self.modules = Module.objects.filter(windows=window)
        self.assessors = Assessor.objects.filter(windows=window)
        self.helpers = Helper.objects.filter(windows=window)
        self.block_slots = BlockSlot.objects.filter(window=window)
        self.block_templates = BlockTemplate.objects.filter(windows=self.window)

        self.workload_calc = workload_calculator or WorkloadCalculator(
            exams=self.exams,
            assessors=self.assessors,
            block_templates=self.block_templates
        )

    def collect(self) -> InputData:
        return InputData(
            exams=self.exams,
            modules=self.modules,
            assessors=self.assessors,
            assessor_workload=self.workload_calc.assessor_block_counts,
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
