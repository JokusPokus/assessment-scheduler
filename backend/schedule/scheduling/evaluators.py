"""
Feasibility and quality evaluation of schedules.
"""
from abc import ABC, abstractmethod
from collections import defaultdict
from functools import lru_cache
from pprint import pprint
from typing import List, Optional, Dict, Tuple

from django.db.models import QuerySet

from exam.models import Exam, Student
from schedule.models import BlockSlot
from staff.models import Assessor, Helper

from .schedule import Schedule, ExamSchedule, BlockSchedule
from .input_collectors import InputData
from .types import ExamId


class ConflictDegree:
    FIRST_ORDER = 0
    SHORTLY_FOLLOWED = 1
    SAME_DAY = 2
    CONSECUTIVE_DAYS = 3


class Conflict:
    """Represents a first-order conflict in a schedule, that is,
    a student being scheduled for more than one exam at the same time.
    """

    def __init__(
            self,
            exams: List[ExamSchedule],
    ):
        self.exams = exams

    def __repr__(self):
        first, second = self.exams
        return f"<{first} vs. {second}>"


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
        *  'shortly_followed': a student is scheduled for two exams with
           less than three hours in between.
        *  'same_day': a student has two exams on the same day.
        *  'consecutive_days': a student has two exams on consecutive days.
        """
        pass


class BruteForce(ConflictSearch):
    """Simple brute-force algorithm to find conflicting time frames."""

    def run(
            self,
            by_student: Dict[Student, List[ExamSchedule]],
    ) -> Dict[Student, Dict[int, List[Conflict]]]:
        conflicts = defaultdict(lambda: defaultdict(list))

        for student, exams in by_student.items():
            exams.sort()

            for i, first in enumerate(exams[:-1]):
                for second in exams[i + 1:]:
                    category = self._get_conflict_category(first, second)

                    if category is None:
                        continue

                    conflicts[student][category].append(
                        Conflict(
                            exams=[first, second],
                        )
                    )

        return conflicts

    @staticmethod
    def _get_conflict_category(
            first: ExamSchedule,
            second: ExamSchedule
    ) -> Optional[int]:
        """If a conflict is found between the exam schedules, return the
        category of the conflict. Else, return None.
        """
        if first.time_frame.overlaps_with(second.time_frame):
            return ConflictDegree.FIRST_ORDER

        if first.time_frame.shortly_followed_by(second.time_frame):
            return ConflictDegree.SHORTLY_FOLLOWED

        if first.time_frame.same_day_as(second.time_frame):
            return ConflictDegree.SAME_DAY

        if first.time_frame.on_consecutive_days(second.time_frame):
            return ConflictDegree.CONSECUTIVE_DAYS

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

    def conflicts(
            self,
            schedule: Schedule
    ) -> Dict[Student, Dict[int, List[Conflict]]]:
        """Return a dictionary of conflicts found in the given schedule,
        split by conflict category and student.
        """
        by_student = schedule.group_by_student()
        return self.conflict_search.run(by_student)

    def penalty(self, schedule: Schedule) -> int:
        """Return the penalty value (the value of the objective function)
        for a given schedule.
        """
        penalties = self._penalties_by_student(schedule)
        return sum([penalty for _, penalty in penalties])

    def most_conflicted_student(self, schedule: Schedule) -> Student:
        """Return the student who scores the highest penalty."""
        penalties = self._penalties_by_student(schedule)
        return max(penalties, key=lambda x: x[1])[0]

    def most_conflicted_block(self, schedule: Schedule) -> BlockSchedule:
        pass

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

    @lru_cache
    def _penalties_by_student(
            self,
            schedule: Schedule
    ) -> List[Tuple[Student, int]]:
        def total_penalty(student_conf: Dict[int, List[Conflict]]) -> int:
            """Return a given student's total penalty."""
            return sum([
                len(student_conf[ConflictDegree.FIRST_ORDER]) * self.penalty_0,
                len(student_conf[ConflictDegree.SHORTLY_FOLLOWED]) * self.penalty_1,
                len(student_conf[ConflictDegree.SAME_DAY]) * self.penalty_2,
                len(student_conf[ConflictDegree.CONSECUTIVE_DAYS]) * self.penalty_3
            ])

        return [
            (student, total_penalty(conf))
            for student, conf in self.conflicts(schedule).items()
        ]
