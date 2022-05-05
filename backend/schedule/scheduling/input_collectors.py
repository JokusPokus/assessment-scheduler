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

from .types import AssessorBlockCounts, StaffAvails


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
    staff_avails: StaffAvails
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
        """Return the number of blocks each assessor has to execute
        if exams are assigned as efficiently as possible, as a function
        of exam length.
        """
        return {
            assessor.email: self._get_block_counts_for(assessor)
            for assessor in self.assessors
        }

    def _get_block_counts_for(self, assessor: Assessor):
        """Calculate the number of blocks the assessor has to execute
        as a function of exam length and return the result as a dictionary.
        """
        def block_count_for(exam_length) -> int:
            standard_count = exams.filter(
                style=ExamStyle.STANDARD,
                module__standard_length=exam_length,
            ).count()
            alt_count = exams.filter(
                style=ExamStyle.ALTERNATIVE,
                module__alternative_length=exam_length
            ).count()

            total_count = standard_count + alt_count
            return math.ceil(total_count / exams_per_block[exam_length])

        exams = self.exams.filter(assessor=assessor)
        exams_per_block = {
            length: self._exams_per_block_of(length)
            for length in self._exam_lengths
        }

        return {
            length: count
            for length in self._exam_lengths
            if (count := block_count_for(length))
        }

    def _exams_per_block_of(self, length) -> int:
        template = self.block_templates.get(exam_length=length)
        exams_per_block = len(template.exam_start_times)
        return exams_per_block

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
            staff_avails=self._staff_avails,
            block_slots=self.block_slots,
            block_templates=self.block_templates,
        )

    @property
    def _staff_avails(self) -> StaffAvails:
        """Return the number and email ids of available helpers
        and assessors per block slot.
        """
        return {
            slot.id: {
                'helper_count': slot.helper.count(),
                'helpers': list(slot.helper.all()),
                'assessor_count': slot.assessor.count(),
                'assessors': list(slot.assessor.all()),
            }
            for slot in self.block_slots
            if slot.assessor.exists()
        }
