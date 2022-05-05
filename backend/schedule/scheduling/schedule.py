"""
Schedule specification.
"""
from collections import UserDict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from exam.models import Student
from staff.models import Assessor, Helper

from .types import SlotId


@dataclass
class ExamSchedule:
    """Represents the schedule of a single exam."""

    exam_code: str
    position: int
    student: Student


@dataclass
class BlockSchedule:
    """Represents the schedule of a block of exams."""

    start_time: datetime
    exam_start_times: List[timedelta]
    assessor: Assessor
    exam_length: int
    exams: List[ExamSchedule] = field(default_factory=list)
    helper: Optional[Helper] = None


class Schedule(UserDict):
    """Represents a complete window schedule."""

    def __setitem__(self, key, value):
        if not isinstance(key, SlotId):
            raise ValueError(
                f"The key must be of type str, not {type(key)}."
            )
        if not isinstance(value, BlockSchedule):
            raise ValueError(
                f"The value must be of type BlockSchedule, not {type(value)}."
            )
        self.data[key] = value
