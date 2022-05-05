"""
Feasibility and quality evaluation of schedules.
"""
from typing import List

from django.db.models import QuerySet

from exam.models import Exam, Student
from schedule.models import BlockSlot

from .schedule import Schedule


class Conflict:
    """Represents a first-order conflict in a schedule, that is,
    a student being scheduled for more than one exam at the same time.
    """
    def __init__(
            self,
            exams: List[Exam],
            student: Student,
            block_slot: BlockSlot
    ):
        self.exams = exams
        self.student = student
        self.block_slot = block_slot


class Evaluator:
    """Provides evaluation methods to check if a proposed solution
    violates first-order constraints and quantifies a schedule's
    quality.
    """

    @staticmethod
    def first_order_conflicts(schedule: Schedule) -> List[Conflict]:
        """Return a list of first-order conflicts found in the
        given schedule.

        A first-order conflict exists if a student or assessor
        is scheduled for two exams with overlapping time frames.
        """
        schedule.group_by_start_time()
