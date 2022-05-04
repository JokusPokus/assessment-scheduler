"""
Implementation of the Tabu Search (TS) meta heuristic.
"""
from datetime import datetime, timedelta

from .base import BaseAlgorithm, RandomAssignment
from ..types import Schedule


class TabuSearch(BaseAlgorithm):
    """Tabu search is a local meta heuristic that iteratively explores
    the solution space while keeping track of a 'tabu list'.
    """

    def run(self) -> Schedule:
        schedule = RandomAssignment(self.data).run()

        while self.evaluator.first_order_conflicts(schedule):
            self._iterate(schedule)

        return schedule
