"""
Abstract base class for algorithm implementations.
"""
from abc import ABC, abstractmethod
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
        self.data = data
        self.evaluator = evaluator

    @abstractmethod
    def run(self) -> Schedule:
        """Solve the exam scheduling problem as defined by self.data and
        return the solution as a Schedule instance.
        """
        pass
