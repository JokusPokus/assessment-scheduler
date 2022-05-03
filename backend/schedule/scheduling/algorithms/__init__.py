"""
Implementations of planning algorithms to solve the exam scheduling
problem.
"""
from abc import ABC, abstractmethod

from ..input_collectors import InputData


class Schedule:
    pass


class BaseAlgorithm(ABC):
    """Defines an interface for Algorithm implementations."""

    def __init__(self, data: InputData):
        self.data = data

    @abstractmethod
    def run(self) -> Schedule:
        """Solve the exam scheduling problem as defined by self.data and
        return the solution as a Schedule instance.
        """
        pass
