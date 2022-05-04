"""
Abstract base class for algorithm implementations.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict, Dict

from ..input_collectors import InputData
from ..evaluators import Evaluator
from ..types import Schedule


class BaseAlgorithm(ABC):
    """Defines an interface for Algorithm implementations."""

    def __init__(self, data: InputData, evaluator: Evaluator):
        self.data = data
        self.evaluator = evaluator

    @abstractmethod
    def run(self) -> Schedule:
        """Solve the exam scheduling problem as defined by self.data and
        return the solution as a Schedule instance.
        """
        pass
