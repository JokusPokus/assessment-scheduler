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
