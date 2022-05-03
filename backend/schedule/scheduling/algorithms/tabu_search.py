"""
Implementation of Tabu Search (TS) meta heuristic.
"""
from datetime import datetime

from .base import BaseAlgorithm, Schedule


class TabuSearch(BaseAlgorithm):
    def run(self) -> Schedule:
        return {
            exam.code: {
                'start_time': datetime.now(),
                'end_time': datetime.now(),
                'helper': 'helper@code.berlin'
            }
            for exam in self.data.exams
        }
