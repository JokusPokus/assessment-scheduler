"""
Useful type specification for the scheduling process.
"""
from datetime import datetime, timedelta
from typing import Dict, TypedDict, List, Optional

from exam.models import Student
from staff.models import Helper, Assessor


SlotId = int
Email = int
ExamId = str
ExamLength = int
Count = int
BlockCount = Dict[ExamLength, Count]
AssessorBlockCounts = Dict[Email, BlockCount]


class AvailInfo(TypedDict):
    """Data about the number and email ids of helpers available
    in a given block slot.
    """
    helper_count: int
    helpers: List[Helper]
    assessor_count: int
    assessors: List[Assessor]


class ExamSchedule(TypedDict):
    exam: ExamId
    position: int
    student: Student


class BlockSchedule(TypedDict):
    start_time: datetime
    exam_start_times: List[timedelta]
    assessor: Assessor
    helper: Optional[Helper]
    exam_length: int
    exams: List[ExamSchedule]


class Conflict(TypedDict):
    exams: List[ExamId]
    student: Email


StaffAvails = Dict[SlotId, AvailInfo]
Schedule = Dict[SlotId, List[BlockSchedule]]
