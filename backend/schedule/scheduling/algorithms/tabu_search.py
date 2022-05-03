"""
Implementation of Tabu Search (TS) meta heuristic.
"""
from . import BaseAlgorithm, Schedule


class TabuSearch(BaseAlgorithm):
    def run(self) -> Schedule:
        raise NotImplementedError
