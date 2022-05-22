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
from uuid import uuid4

from exam.models import Student, Module
from staff.models import Assessor, Helper

from .types import SlotId


MINIMAL_DESIRABLE_BREAK = timedelta(minutes=180)


class TimeFrame:
    """A time frame specified by its start and end time."""

    def __init__(self, start_time: datetime, end_time: datetime):
        self.start_time = start_time
        self.end_time = end_time

    def __eq__(self, other):
        return (
            self.start_time == other.start_time
            and self.end_time == other.end_time
        )

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
                not self.start_time >= other.end_time
                and not other.start_time >= self.end_time
        )

    def shortly_followed_by(self, other: TimeFrame) -> bool:
        """Return True if other's start time follows self's end time, but
        by less than the specified minimal break.
        """
        if self.end_time > other.start_time:
            return False

        _break = other.start_time - self.end_time
        return _break < MINIMAL_DESIRABLE_BREAK

    def same_day_as(self, other: TimeFrame) -> bool:
        """Return True if the two time frames' start times are on the same
        day.
        """
        return self.start_time.date() == other.start_time.date()

    def on_consecutive_days(self, other: TimeFrame) -> bool:
        """Return True if the two time frames' start times are on consecutive
        days.
        """
        day_distance = abs(self.start_time.date() - other.start_time.date())
        return day_distance == timedelta(days=1)


@dataclass
class ExamSchedule:
    """Represents the schedule of a single exam."""

    exam_code: str
    module: Module
    position: int
    student: Student
    time_frame: TimeFrame

    def __repr__(self):
        return f'{self.position+1}. {self.exam_code} ({self.module.code}): ' \
               f'{self.student.email}'

    def __lt__(self, other):
        return self.time_frame < other.time_frame

    def __eq__(self, other):
        return (
            self.exam_code == other.exam_code
            and self.time_frame == other.time_frame
        )


@dataclass
class BlockSchedule:
    """Represents the schedule of a block of exams."""

    assessor: Assessor
    start_time: Optional[datetime] = None
    exam_start_times: List[int] = field(default_factory=list)
    exam_length: Optional[int] = None
    exams: List[ExamSchedule] = field(default_factory=list)
    helper: Optional[Helper] = None

    def __repr__(self):
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pformat(
            {
                'start_time': self.start_time.strftime('%d.%m. %H:%M') if self.start_time else 't.b.d',
                'assessor': self.assessor.email,
                'helper': self.helper.email if self.helper else 't.b.d.',
                'exams': self.exams or 't.b.d'
            }
        )

    def __eq__(self, other):
        return (
            self.assessor.id == other.assessor.id
            and self.start_time == other.start_time
            and self.exam_start_times == other.exam_start_times
            and self.exams == other.exams
            and self.helper == other.helper
        )

    @property
    def start_times(self) -> List[datetime]:
        """Return a list of datetime objects, where each one represents
        a start time in this block"""
        assert self.start_time, 'No start time given yet'

        num_scheduled_exams = len(self.exams)
        return [
            self.start_time + timedelta(minutes=offset)
            for offset in self.exam_start_times[:num_scheduled_exams]
        ]

    @property
    def delta(self) -> timedelta:
        """Return a timedelta with the size of the block's exam length."""
        return timedelta(minutes=self.exam_length)


class Schedule(UserDict):
    """Represents a complete window schedule.

    Each key is a slot id and its value is a list of BlockSchedules.
    """
    def __init__(self):
        super().__init__(self)
        self.__key = uuid4()

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
        if key not in self.data:
            self.data[key] = []

        return self.data[key]

    def __hash__(self):
        return hash(self.__key)

    def __eq__(self, other):
        return self.__key == other.__key

    def __str__(self):
        pp = pprint.PrettyPrinter()
        return pp.pformat(self.data)

    def group_by_student(self) -> Dict[Student, List[ExamSchedule]]:
        """Return the schedule transformed in such a way that each
        key represents a student. Its value is a list of (start_time, end_time)
        tuples each representing one of that student's exams.
        """
        by_student = defaultdict(list)

        lists_of_blocks = self.data.values()
        for block in itertools.chain(*lists_of_blocks):
            for exam in block.exams:
                by_student[exam.student].append(exam)

        return by_student

    @property
    def total_blocks_scheduled(self) -> int:
        """Return the number of total blocks in this schedule."""
        return sum([len(block_list) for block_list in self.data.values()])
