"""
Input collection to working memory for scheduling purposes
"""
from abc import ABC, abstractmethod
from collections import UserDict
from dataclasses import dataclass
import math
from typing import Dict, TypedDict, List

from django.db.models import QuerySet

from schedule.models import Window, BlockSlot, BlockTemplate
from exam.models import Exam, Module, Student, ExamStyle
from staff.models import Assessor, Helper

from .types import SlotId


@dataclass
class AvailInfo:
    """Data about the number and email ids of helpers available
    in a given block slot.
    """
    helper_count: int
    helpers: List[Helper]
    assessor_count: int
    assessors: List[Assessor]

    def remove(self, assessor) -> None:
        """Remove the assessor from the assessors list and decrement the
        assessor count by 1.

        If this leads to no remaining availabilities, delete the assessor
        from the list (or delete an empty list altogether).
        """
        if assessor not in self.assessors:
            raise ValueError(
                f'The assessor {assessor} was not found in the list'
            )

        self.assessors.remove(assessor)
        self.assessor_count -= 1


class AssessorWorkload(UserDict):
    """Represents the workload in blocks of a single assessor, grouped by
    the block's exam length.

    For example, self.data could look like this:
    {
        <Assessor 1>: {
            20: 2,
            30: 5
        },
        <Assessor 2>: {
            20: 4
        },
        ...
    }
    """
    def __setitem__(self, key, value):
        if not isinstance(key, Assessor):
            raise TypeError(
                f'The key must be an Assessor instance, not {type(key)}'
            )

        if not isinstance(value, dict):
            raise TypeError(
                f'The value must be a dict, not {type(value)}'
            )

        self.data[key] = value

    def decrement(self, assessor, exam_length):
        """Decrement the assessor's workload for the given exam_length
        by one block.
        """
        if assessor not in self.data:
            raise ValueError(
                f'The assessor {assessor} is not considered for this schedule'
            )

        if exam_length not in self.data[assessor]:
            raise ValueError(
                f'The assessor has no {exam_length}-minute exams'
            )

        self.data[assessor][exam_length] -= 1

    def remaining_blocks_of(self, assessor: Assessor) -> int:
        """Return the number of blocks remaining to be scheduled for
        the assessor.
        """
        return sum(self.data[assessor].values())


@dataclass
class InputData:
    """Defines the input data requirements for
    any scheduling algorithm.
    """

    window: Window
    exams: QuerySet
    modules: QuerySet
    assessors: QuerySet
    assessor_workload: AssessorWorkload
    helpers: QuerySet
    staff_avails: Dict[SlotId, AvailInfo]
    block_slots: QuerySet
    block_templates: QuerySet
    total_num_blocks: int


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
    def assessor_block_counts(self) -> AssessorWorkload:
        """Return the number of blocks each assessor has to execute
        if exams are assigned as efficiently as possible, as a function
        of exam length.
        """
        workload = AssessorWorkload()
        workload.update({
            assessor: self._get_block_counts_for(assessor)
            for assessor in self.assessors
        })
        return workload

    def _get_block_counts_for(self, assessor: Assessor) -> Dict[int, int]:
        """Calculate the number of blocks the assessor has to execute
        as a function of exam length and return the result as a dictionary.
        """
        def block_count_for(exam_length) -> int:
            """Return an assessor's total count of blocks filled by exams
            of the given exam_length.

            Even if a block is not entirely filled with exams, it counts as a
            complete block to be scheduled.
            """
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
        """Return the number of exams per block of the given exam length."""
        template = self.block_templates.get(exam_length=length)
        exams_per_block = len(template.exam_start_times)
        return exams_per_block

    @property
    def _exam_lengths(self) -> set:
        """Return the set of exam lengths that are considered for
        this scheduling window.
        """
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
        self.assessor_workload = self.workload_calc.assessor_block_counts

    def collect(self) -> InputData:
        return InputData(
            window=self.window,
            exams=self.exams,
            modules=self.modules,
            assessors=self.assessors,
            assessor_workload=self.assessor_workload,
            helpers=self.helpers,
            staff_avails=self._staff_avails,
            block_slots=self.block_slots,
            block_templates=self.block_templates,
            total_num_blocks=self._total_num_blocks
        )

    @property
    def _staff_avails(self) -> Dict[SlotId, AvailInfo]:
        """Return the number and email ids of available helpers
        and assessors per block slot.
        """
        return {
            slot.id: AvailInfo(
                helper_count=slot.helper.count(),
                helpers=list(slot.helper.all()),
                assessor_count=slot.assessor.count(),
                assessors=list(slot.assessor.all()),
            )
            for slot in self.block_slots
            if slot.assessor.exists()
        }

    @property
    def _total_num_blocks(self) -> int:
        """Return the total number of blocks that need to be scheduled,
        that is, the sum of individual assessors' blocks.
        """
        return sum(
            [
                sum(block_count.values())
                for block_count in self.assessor_workload.values()
            ]
        )
