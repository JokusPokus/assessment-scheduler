"""
Implementation of the Tabu Search (TS) meta heuristic.
"""
from datetime import datetime

from .base import BaseAlgorithm, Schedule


class TabuSearch(BaseAlgorithm):
    """Tabu search is a local meta heuristic that iteratively explores
    the solution space while keeping track of a 'tabu list'.
    """

    def run(self) -> Schedule:
        return {
            exam.code: {
                'start_time': datetime.now(),
                'end_time': datetime.now(),
                'helper': 'helper@code.berlin'
            }
            for exam in self.data.exams
        }
