"""
Useful type specification for the scheduling process.
"""
from datetime import datetime
from typing import Dict, TypedDict, List


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
    count: int
    helpers: List[Email]


class ScheduledInfo(TypedDict):
    start_time: datetime
    end_time: datetime
    helper: Email


HelperAvails = Dict[SlotId, AvailInfo]
Schedule = Dict[ExamId, ScheduledInfo]
