"""
Abstract base class for algorithm implementations.
"""
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Optional

from ..input_collectors import InputData
from ..evaluators import Evaluator
from ..schedule import Schedule


class BaseAlgorithm(ABC):
    """Defines an interface for algorithm implementations."""

    def __init__(
            self,
            data: InputData,
            evaluator: Optional[Evaluator] = None
    ):
        self.data = deepcopy(data)
        self.evaluator = evaluator

    @abstractmethod
    def run(self) -> Schedule:
        """Solve the exam scheduling problem as defined by self.data and
        return the solution as a Schedule instance.
        """
        pass


class UnfeasibleInputError(BaseException):
    """Raised by back-tracking algorithm if the staff availabilities
    and workloads do not allow for a valid schedule.
    """
    pass
