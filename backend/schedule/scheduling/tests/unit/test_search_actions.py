import pytest

from copy import deepcopy
from datetime import datetime

from exam.models import Student, Module
from staff.models import Assessor

from schedule.scheduling.algorithms.tabu_search import Actions
from schedule.scheduling.schedule import (
    Schedule,
    BlockSchedule,
    ExamSchedule,
    TimeFrame,
)


pytestmark = pytest.mark.unit


class TestSearchActions:
    def test_blocks_are_swapped(self):
        # ARRANGE
        schedule = Schedule()

        student = Student(id=1)

        block_1_time_frames = [
            TimeFrame(
                datetime(2022, 1, 1, 10, 0),
                datetime(2022, 1, 1, 10, 30),
            ),
            TimeFrame(
                datetime(2022, 1, 1, 10, 30),
                datetime(2022, 1, 1, 11, 0),
            ),
        ]
        block_2_time_frames = [
            TimeFrame(
                datetime(2022, 1, 2, 14, 0),
                datetime(2022, 1, 2, 14, 20),
            ),
            TimeFrame(
                datetime(2022, 1, 1, 14, 20),
                datetime(2022, 1, 1, 14, 40),
            ),
            TimeFrame(
                datetime(2022, 1, 1, 14, 40),
                datetime(2022, 1, 1, 15, 0),
            ),
        ]
        block_3_time_frames = [
            TimeFrame(
                datetime(2022, 1, 1, 10, 0),
                datetime(2022, 1, 1, 10, 30),
            ),
            TimeFrame(
                datetime(2022, 1, 1, 10, 30),
                datetime(2022, 1, 1, 11, 0),
            ),
        ]

        block_1_exams = [
            ExamSchedule(
                student=student,
                position=0,
                module=Module(),
                exam_code='exam_1_1',
                time_frame=block_1_time_frames[0]
            ),
            ExamSchedule(
                student=student,
                position=1,
                module=Module(),
                exam_code='exam_1_2',
                time_frame=block_1_time_frames[1]
            ),
        ]

        block_2_exams = [
            ExamSchedule(
                student=student,
                position=0,
                module=Module(),
                exam_code='exam_2_1',
                time_frame=block_2_time_frames[0]
            ),
            ExamSchedule(
                student=student,
                position=1,
                module=Module(),
                exam_code='exam_2_2',
                time_frame=block_2_time_frames[1]
            ),
            ExamSchedule(
                student=student,
                position=2,
                module=Module(),
                exam_code='exam_2_3',
                time_frame=block_2_time_frames[2]
            ),
        ]

        block_3_exams = [
            ExamSchedule(
                student=student,
                position=0,
                module=Module(),
                exam_code='exam_3_1',
                time_frame=block_3_time_frames[0]
            ),
            ExamSchedule(
                student=student,
                position=1,
                module=Module(),
                exam_code='exam_3_2',
                time_frame=block_3_time_frames[1]
            ),
        ]

        block_1 = BlockSchedule(assessor=Assessor(), exams=block_1_exams)
        block_2 = BlockSchedule(assessor=Assessor(), exams=block_2_exams)
        block_3 = BlockSchedule(assessor=Assessor(), exams=block_3_exams)

        # To verify later that this block is not modified
        block_3_deepcopy = deepcopy(block_3)

        schedule[0] = [block_1, block_3]
        schedule[1] = [block_2]

        # ACT
        new_schedule = Actions().swap_blocks(
            schedule=schedule,
            blocks=[(0, block_1), (1, block_2)]
        )

        # ASSERT
        # The original schedule has not been changed
        assert schedule != new_schedule
        assert schedule[0] == [block_1, block_3]
        assert schedule[1] == [block_2]

        # Block 3 in the new schedule has not been changed
        assert new_schedule[0][0] == block_3_deepcopy


