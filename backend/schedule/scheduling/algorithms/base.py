"""
Abstract base class for algorithm implementations.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict, Dict

from ..input_collectors import InputData


ExamId = str
Email = str


class ScheduledInfo(TypedDict):
    start_time: datetime
    end_time: datetime
    helper: Email


Schedule = Dict[ExamId, ScheduledInfo]


class BaseAlgorithm(ABC):
    """Defines an interface for Algorithm implementations."""

    def __init__(self, data: InputData, validator):
        self.data = data
        self.validator = validator

    @abstractmethod
    def run(self) -> Schedule:
        """Solve the exam scheduling problem as defined by self.data and
        return the solution as a Schedule instance.
        """
        pass
