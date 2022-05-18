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
                datetime(2022, 1, 2, 14, 20),
                datetime(2022, 1, 2, 14, 40),
            ),
            TimeFrame(
                datetime(2022, 1, 2, 14, 40),
                datetime(2022, 1, 2, 15, 0),
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

        block_1 = BlockSchedule(
            assessor=Assessor(),
            exams=block_1_exams,
            exam_length=30,
            start_time=block_1_time_frames[0].start_time,
            exam_start_times=[0, 30]
        )
        block_2 = BlockSchedule(
            assessor=Assessor(),
            exams=block_2_exams,
            exam_length=20,
            start_time=block_2_time_frames[0].start_time,
            exam_start_times=[0, 20, 40]
        )
        block_3 = BlockSchedule(
            assessor=Assessor(),
            exams=block_3_exams,
            exam_length=30,
            start_time=block_3_time_frames[0].start_time,
            exam_start_times=[0, 30]
        )

        schedule[0] = [block_1, block_3]
        schedule[1] = [block_2]

        # To verify later that the original schedule is not modified
        schedule_deepcopy = deepcopy(schedule)

        # ACT
        new_schedule = Actions().swap_blocks(
            schedule=schedule,
            block_indeces=[(0, 0), (1, 0)]
        )

        # ASSERT
        # The original schedule has not been changed
        assert schedule == schedule_deepcopy
        assert schedule[0] == [block_1, block_3]
        assert schedule[1] == [block_2]

        # Block 3 in the new schedule has not been changed
        new_block_3 = new_schedule[0][0]
        old_block_3 = schedule_deepcopy[0][1]
        assert new_block_3 == old_block_3

        # Block 1 and 2 have been swapped and updated correctly
        new_block_1 = new_schedule[1][0]
        assert new_block_1.start_time == block_2.start_time
        assert new_block_1.exam_length == block_1.exam_length

        delta = block_2.start_time - block_1.start_time
        for new_exam, old_exam in zip(new_block_1.exams, block_1.exams):
            expected_start_time = old_exam.time_frame.start_time + delta
            expected_end_time = expected_start_time + block_1.delta
            assert new_exam.time_frame.start_time == expected_start_time
            assert new_exam.time_frame.end_time == expected_end_time

        new_block_2 = new_schedule[0][1]
        assert new_block_2.start_time == block_1.start_time
        assert new_block_2.exam_length == block_2.exam_length

        for new_exam, old_exam in zip(new_block_2.exams, block_2.exams):
            expected_start_time = old_exam.time_frame.start_time - delta
            expected_end_time = expected_start_time + block_2.delta
            assert new_exam.time_frame.start_time == expected_start_time
            assert new_exam.time_frame.end_time == expected_end_time
