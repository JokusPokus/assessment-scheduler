"""
Feasibility and quality evaluation of schedules.
"""
from abc import ABC, abstractmethod
from collections import defaultdict
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
    def run(
            by_student: Dict[Student, List[ExamSchedule]],
    ) -> Dict[str, List[Conflict]]:
        """Return a dictionary of conflicts found in the given schedule.

        Each key indicates a category of conflicts with different degrees
        of severity:

        *  'first_order': a student is scheduled for two exams with
           overlapping time frames.
        *  'three_hour': a student is scheduled for two exams with less than
           three hours in between.
        *  'same_day': a student has two exams on the same day.
        *  'consecutive_days': a student has two exams on consecutive days.
        """
        pass


class BruteForce(ConflictSearch):
    """Simple brute-force algorithm to find conflicting time frames."""

    def run(
            self,
            by_student: Dict[Student, List[ExamSchedule]],
    ) -> Dict[str, List[Conflict]]:
        conflicts = defaultdict(list)

        for student, exams in by_student.items():
            exams.sort()

            for i, first in enumerate(exams[:-1]):
                for second in exams[i + 1:]:
                    category = self._get_conflict_category(first, second)

                    if not category:
                        continue

                    conflicts[category].append(
                        Conflict(
                            exams=[first.exam_code, second.exam_code],
                            student=student
                        )
                    )

        return conflicts

    @staticmethod
    def _get_conflict_category(
            first: ExamSchedule,
            second: ExamSchedule
    ) -> Optional[str]:
        """If a conflict is found between the exam schedules, return the
        category of the conflict. Else, return None.
        """
        if first.time_frame.overlaps_with(second.time_frame):
            return 'first_order'

        if first.time_frame.shortly_followed_by(second.time_frame):
            return 'shortly_followed'

        if first.time_frame.same_day_as(second.time_frame):
            return 'same_day'

        if first.time_frame.on_consecutive_days(second.time_frame):
            return 'consecutive_days'

        return None


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
    penalty_0 = 300
    penalty_1 = 100
    penalty_2 = 10
    penalty_3 = 1

    def __init__(self, conflict_search: Optional[ConflictSearch] = None):
        self.conflict_search = conflict_search or BruteForce()

    def conflicts(self, schedule: Schedule) -> Dict[str, List[Conflict]]:
        """Return a dictionary of conflicts found
        in the given schedule.
        """
        by_student = schedule.group_by_student()
        return self.conflict_search.run(by_student)

    def utility(self, schedule: Schedule) -> int:
        """Return the utility value (the value of the objective function)
        for a given schedule.
        """
        conflicts = self.conflicts(schedule)
        return sum([
            len(conflicts['first_order']) * self.penalty_0,
            len(conflicts['shortly_followed']) * self.penalty_1,
            len(conflicts['same_day']) * self.penalty_2,
            len(conflicts['consecutive_days']) * self.penalty_3,
        ])

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
