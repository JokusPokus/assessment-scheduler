"""
Schedule specification.
"""
from collections import UserDict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import pprint
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

    def __repr__(self):
        return f'{self.position+1}. {self.exam_code}: {self.student.email}'


@dataclass
class BlockSchedule:
    """Represents the schedule of a block of exams."""

    start_time: datetime
    exam_start_times: List[timedelta]
    assessor: Assessor
    exam_length: int
    exams: List[ExamSchedule] = field(default_factory=list)
    helper: Optional[Helper] = None

    def __repr__(self):
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pformat(
            {
                'start_time': self.start_time.strftime('%d.%m. %H:%M'),
                'assessor': self.assessor.email,
                'helper': self.helper.email if self.helper else 't.b.d.',
                'exams': self.exams
            }
        )


class Schedule(UserDict):
    """Represents a complete window schedule."""

    def __setitem__(self, key, value):
        if not isinstance(key, SlotId):
            raise ValueError(
                f"The key must be of type str, not {type(key)}."
            )
        if not isinstance(value, List):
            raise ValueError(
                f"The value must be a list of BlockSchedule, not {type(value)}."
            )
        for elem in value:
            if not isinstance(elem, BlockSchedule):
                raise ValueError(
                    f"All elements in value must be of type BlockSchedule. "
                    f"Detected incompatible type: {type(value)}."
                )

        self.data[key] = value

    def __getitem__(self, key):
        """Make self.data a default dict."""
        if key in self.data:
            return self.data[key]
        return []

    def __str__(self):
        pp = pprint.PrettyPrinter()
        return pp.pformat(self.data)
