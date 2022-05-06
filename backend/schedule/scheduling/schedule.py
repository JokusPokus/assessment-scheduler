"""
Schedule specification.
"""
from __future__ import annotations

from collections import UserDict, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import itertools
import pprint
from typing import Dict, List, Optional, Set

from exam.models import Student
from staff.models import Assessor, Helper

from .types import SlotId


class TimeFrame:
    """A time frame specified by its start and end time."""

    def __init__(self, start_time: datetime, end_time: datetime):
        self.start_time = start_time
        self.end_time = end_time

    def __lt__(self, other):
        return self.start_time < other.start_time

    def __repr__(self):
        return f"{self.start_time.strftime('%d.%m. %H:%M')} - " \
               f"{self.end_time.strftime('%H:%M')}"

    def overlaps_with(self, other: TimeFrame) -> bool:
        """Return True if self and other - both TimeFrames - overlap
        in any way, and False otherwise.

        Being precisely back-to-back does not count as an overlap.
        """
        return (
                self.start_time >= other.end_time
                or other.start_time >= self.end_time
        )


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
    exam_start_times: List[int]
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

    @property
    def start_times(self) -> List[datetime]:
        """Return a list of datetime objects, where each one represents
        a start time in this block"""
        num_scheduled_exams = len(self.exams)
        return [
            self.start_time + timedelta(minutes=offset)
            for offset in self.exam_start_times[:num_scheduled_exams]
        ]


class Schedule(UserDict):
    """Represents a complete window schedule.

    Each key is a slot id and its value is a list of BlockSchedules.
    """

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

    def group_by_student(self) -> Dict[Student, List[TimeFrame]]:
        """Return the schedule transformed in such a way that each
        key represents a student. Its value is a list of (start_time, end_time)
        tuples each representing one of that student's exams.
        """
        by_student = defaultdict(list)

        lists_of_blocks = self.data.values()
        for block in itertools.chain(*lists_of_blocks):
            for start_time, exam in zip(block.start_times, block.exams):
                by_student[exam.student].append(
                    TimeFrame(
                        start_time,
                        start_time + timedelta(minutes=block.exam_length)
                    )
                )

        return by_student
