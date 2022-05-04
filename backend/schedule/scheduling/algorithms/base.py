"""
Abstract base class for algorithm implementations.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from ..input_collectors import InputData
from ..evaluators import Evaluator
from ..types import Schedule


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


class RandomAssignment(BaseAlgorithm):
    """Utility class for algorithm initialization."""

    def run(self) -> Schedule:
        """Randomly assign assessor blocks to available slots, and
        then exams to the blocks.

        Return the resulting schedule, which is not guaranteed to be
        free of first-order conflicts.
        """
        return {
            exam.code: {
                'start_time': datetime.now(),
                'length': timedelta(minutes=20),
                'student': 'student@code.berlin',
                'assessor': 'assessor@code.berlin',
            }
            for exam in self.data.exams
        }
