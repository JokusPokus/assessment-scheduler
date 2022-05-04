"""
Implementation of the Tabu Search (TS) meta heuristic.
"""
from datetime import datetime, timedelta

from .base import BaseAlgorithm
from ..types import Schedule


class TabuSearch(BaseAlgorithm):
    """Tabu search is a local meta heuristic that iteratively explores
    the solution space while keeping track of a 'tabu list'.
    """

    def run(self) -> Schedule:
        schedule = self._get_random_initialization()

        while self.evaluator.has_first_order_conflicts(schedule):
            self._iterate(schedule)

        return schedule

    def _get_random_initialization(self) -> Schedule:
        return {
            exam.code: {
                'start_time': datetime.now(),
                'length': timedelta(minutes=20),
                'student': 'student@code.berlin',
                'assessor': 'assessor@code.berlin',
            }
            for exam in self.data.exams
        }
