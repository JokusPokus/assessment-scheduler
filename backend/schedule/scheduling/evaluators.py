"""
Feasibility and quality evaluation of schedules.
"""
from abc import ABC, abstractmethod
from pprint import pprint
from typing import List, Optional

from django.db.models import QuerySet

from exam.models import Exam, Student
from schedule.models import BlockSlot

from .schedule import Schedule, ExamSchedule
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
