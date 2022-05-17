"""
Feasibility and quality evaluation of schedules.
"""
from abc import ABC, abstractmethod
from pprint import pprint
from typing import List, Optional, Dict

from django.db.models import QuerySet

from exam.models import Exam, Student
from schedule.models import BlockSlot
from staff.models import Assessor, Helper

from .schedule import Schedule, ExamSchedule
from .input_collectors import InputData
from .types import ExamId


class Conflict:
    """Represents a first-order conflict in a schedule, that is,
    a student being scheduled for more than one exam at the same time.
    """
    def __init__(
            self,
            exams: List[ExamId],
            student: Student,
    ):
        self.exams = exams
        self.student = student

    def __repr__(self):
        first, second = self.exams
        return f"<{self.student.id}: {first} vs. {second}>"


class ConflictSearch(ABC):
    """Defines an interface for conflict search algorithms."""

    @staticmethod
    @abstractmethod
    def run(student: Student, exams: List[ExamSchedule]) -> List[Conflict]:
        """Return a list of conflicts, each one representing a pair
        of overlapping exams in the exams list.
        """
        pass


class BruteForce(ConflictSearch):
    """Simple brute-force algorithm to find conflicting time frames."""

    @staticmethod
    def run(student: Student, exams: List[ExamSchedule]) -> List[Conflict]:
        exams.sort()

        conflicts = []
        for i, first in enumerate(exams[:-1]):
            for second in exams[i+1:]:
                if first.overlaps_with(second):
                    conflicts.append(
                        Conflict(
                            exams=[first.exam_code, second.exam_code],
                            student=student
                        )
                    )

        return conflicts


class ValidationError(BaseException):
    """Raised if given input data does not allow for a feasible schedule."""
    def __init__(
            self,
            insufficient_avails: Optional[Dict] = None,
            helpers_needed: bool = False
    ):
        self.insufficient_avails = insufficient_avails
        self.helpers_needed = helpers_needed


class Evaluator:
    """Provides evaluation methods to check if a proposed solution
    violates first-order constraints and quantifies a schedule's
    quality.
    """

    def __init__(self, conflict_search: Optional[ConflictSearch] = None):
        self.conflict_search = conflict_search or BruteForce()

    def first_order_conflicts(self, schedule: Schedule) -> List[Conflict]:
        """Return a list of first-order conflicts found in the
        given schedule.

        A first-order conflict exists if a student or assessor
        is scheduled for two exams with overlapping time frames.
        """
        by_student = schedule.group_by_student()

        conflicts = []
        for student, exams in by_student.items():
            student_conflicts = self.conflict_search.run(student, exams)
            conflicts.extend(student_conflicts)

        return conflicts

    def validate_availabilities(self, data: InputData) -> None:
        """Raise a validation error if the given staff availabilities
        do not allow for a feasible schedule.

        This happens in any of the following cases:
        (1) any assessor has less available slots than blocks to be scheduled
        (2) the total helper availabilities are less than the total blocks
            to be scheduled, where an 'unnecessary' helper-over-assessor
            availability surplus does not count (i.e., there is no use in
            many available helpers for a given slot if the number of
            available assessors is smaller).
        """
        insufficient_avails = self._get_avail_insufficiencies(data)
        helpers_needed = self._helpers_needed(data)

        if insufficient_avails or helpers_needed:
            raise ValidationError(
                insufficient_avails=insufficient_avails,
                helpers_needed=helpers_needed
            )

    @staticmethod
    def _helpers_needed(data) -> bool:
        """Return True if the number of (relevant) helper availabilities
        is smaller than the number of blocks that need to be scheduled.
        Return False otherwise.
        """
        num_blocks_w_potential_helper = sum(
            [
                max(slot.assessor.count(), slot.helper.count())
                for slot in data.block_slots
            ]
        )
        return num_blocks_w_potential_helper < data.total_num_blocks

    @staticmethod
    def _get_avail_insufficiencies(data) -> Dict[Assessor, Dict[str, int]]:
        """Return information about potentially insufficient assessor
        availabilities.
        """
        insufficient_avails = {}

        for assessor, workload in data.assessor_workload.items():
            available_slots = assessor.available_blocks.filter(
                window=data.window
            ).count()
            blocks_to_schedule = sum(workload.values())

            if blocks_to_schedule > available_slots:
                insufficient_avails[assessor] = {
                    'available_slots': available_slots,
                    'blocks_to_schedule': blocks_to_schedule
                }

        return insufficient_avails
