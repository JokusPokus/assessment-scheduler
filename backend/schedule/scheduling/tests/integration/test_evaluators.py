import pytest

from datetime import datetime

from exam.models import Student, Module
from staff.models import Assessor

from schedule.scheduling.evaluators import Evaluator, Conflict, ConflictDegree
from schedule.scheduling.schedule import (
    ExamSchedule,
    BlockSchedule,
    Schedule,
    TimeFrame,
)


pytestmark = pytest.mark.integration


class TestEvaluator:
    def test_first_order_conflicts_are_found(self):
        # ARRANGE
        schedule = Schedule()

        student_1 = Student(id=1)
        student_2 = Student(id=2)
        student_3 = Student(id=3)

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
                datetime(2022, 1, 1, 10, 0),
                datetime(2022, 1, 1, 10, 20),
            ),
            TimeFrame(
                datetime(2022, 1, 1, 10, 20),
                datetime(2022, 1, 1, 10, 40),
            ),
            TimeFrame(
                datetime(2022, 1, 1, 10, 40),
                datetime(2022, 1, 1, 11, 0),
            ),
        ]

        # Create two blocks with two conflicting exams in total:
        # +-----------------------+      +-----------------------+
        # |   30 min, student 1   |      |   20 min, student 1   |
        # |                       |      |_______________________|
        # |_______________________|      |   20 min, student 3   |
        # |   30 min, student 2   |      |_______________________|
        # |                       |      |   20 min, student 2   |
        # |                       |      |                       |
        # +-----------------------+      +-----------------------+

        block_1_exams = [
            ExamSchedule(
                student=student_1,
                position=0,
                module=Module(),
                assessor=Assessor(),
                exam_code='exam_1_1',
                time_frame=block_1_time_frames[0]
            ),
            ExamSchedule(
                student=student_2,
                position=1,
                module=Module(),
                assessor=Assessor(),
                exam_code='exam_1_2',
                time_frame=block_1_time_frames[1]
            ),
        ]

        block_2_exams = [
            ExamSchedule(
                student=student_1,
                position=0,
                module=Module(),
                assessor=Assessor(),
                exam_code='exam_2_1',
                time_frame=block_2_time_frames[0]
            ),
            ExamSchedule(
                student=student_3,
                position=1,
                module=Module(),
                assessor=Assessor(),
                exam_code='exam_2_2',
                time_frame=block_2_time_frames[1]
            ),
            ExamSchedule(
                student=student_2,
                position=2,
                module=Module(),
                assessor=Assessor(),
                exam_code='exam_2_3',
                time_frame=block_2_time_frames[2]
            ),
        ]

        blocks = [
            BlockSchedule(
                assessor=Assessor(),
                exams=block_1_exams
            ),
            BlockSchedule(
                assessor=Assessor(),
                exams=block_2_exams
            )
        ]

        schedule[0] = blocks

        # ACT
        conflicts = Evaluator().conflicts(schedule)

        # ASSERT
        total_first_order_conflicts = sum(
            [
                len(confs[ConflictDegree.FIRST_ORDER])
                for confs in conflicts.values()
            ]
        )
        assert total_first_order_conflicts == 2

        assert conflicts[student_1][ConflictDegree.FIRST_ORDER][0].exams \
            == [block_1_exams[0], block_2_exams[0]]
        assert conflicts[student_2][ConflictDegree.FIRST_ORDER][0].exams \
            == [block_1_exams[1], block_2_exams[2]]
