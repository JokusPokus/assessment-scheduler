"""
Implementation of the Tabu Search (TS) meta heuristic.
"""
from datetime import datetime, timedelta

from .base import BaseAlgorithm
from .random import RandomAssignment
from ..schedule import Schedule, BlockSchedule, ExamSchedule


class TabuSearch(BaseAlgorithm):
    """Tabu search is a local meta heuristic that iteratively explores
    the solution space while keeping track of a 'tabu list'.
    """

    def run(self) -> Schedule:
        schedule = RandomAssignment(self.data).run()

        while self.evaluator.first_order_conflicts(schedule):
            self._iterate(schedule)

        return schedule

    def _iterate(self, schedule: Schedule):
        """Modify the schedule according to the tabu search algorithm, such
        that the resulting schedule is a neighbor of the current one.
        """
        pass
