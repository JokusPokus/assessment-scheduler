"""
Feasibility and quality evaluation of schedules.
"""
from .algorithms.base import Schedule


class Evaluator:
    """Provides evaluation methods to check if a proposed solution
    violates first-order constraints and quantifies a schedule's
    quality.
    """

    @staticmethod
    def has_first_order_conflicts(schedule: Schedule) -> bool:
        """Return True if the given schedule has any first-order
        conflicts and False otherwise.

        A first-order conflict exists if a student or assessor
        is scheduled for two exams with overlapping time frames.
        """
        pass
