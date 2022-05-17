import pytest

from datetime import datetime

from exam.models import Student, Module

from schedule.scheduling.evaluators import BruteForce, Conflict
from schedule.scheduling.schedule import ExamSchedule, TimeFrame

pytestmark = pytest.mark.unit


NON_OVERLAP_TEST_FRAMES = [
    pytest.param(
        TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 20)
        ),
        TimeFrame(
            datetime(2022, 1, 1, 11, 0),
            datetime(2022, 1, 1, 11, 20)
        ),
        id='early_first__disjunct'
    ),
    pytest.param(
        TimeFrame(
            datetime(2022, 1, 1, 11, 0),
            datetime(2022, 1, 1, 11, 40)
        ),
        TimeFrame(
            datetime(2022, 1, 1, 10, 10),
            datetime(2022, 1, 1, 10, 30)
        ),
        id='late_first__disjunct'
    ),
    pytest.param(
        TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 20)
        ),
        TimeFrame(
            datetime(2022, 1, 1, 10, 20),
            datetime(2022, 1, 1, 10, 40)
        ),
        id='back_to_back__early_first'
    ),
    pytest.param(
        TimeFrame(
            datetime(2022, 1, 1, 10, 20),
            datetime(2022, 1, 1, 10, 40)
        ),
        TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 20)
        ),
        id='back_to_back__late_first'
    ),
]


class TestBruteForceAlgorithm:
    def test_existing_conflicts_are_found(self):
        # ARRANGE
        student = Student()

        first_time_frame = TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 30),
        )
        conflicting_time_frame = TimeFrame(
            datetime(2022, 1, 1, 10, 20),
            datetime(2022, 1, 1, 10, 40),
        )

        exams = [
            ExamSchedule(
                student=student,
                position=0,
                module=Module(),
                exam_code='exam_1',
                time_frame=first_time_frame
            ),
            ExamSchedule(
                student=student,
                position=0,
                module=Module(),
                exam_code='exam_2',
                time_frame=conflicting_time_frame
            ),
        ]

        # ACT
        conflicts = BruteForce.run(student, exams)

        # ASSERT
        assert len(conflicts) == 1

        conflict = conflicts[0]
        assert isinstance(conflict, Conflict)
        assert conflict.student == student
        assert set(conflict.exams) == {'exam_1', 'exam_2'}

    def test_conflicts_are_recorded_pairwise(self):
        # ARRANGE
        student = Student()

        first_tf = TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 30),
        )
        second_tf = TimeFrame(
            datetime(2022, 1, 1, 10, 10),
            datetime(2022, 1, 1, 10, 40),
        )
        third_tf = TimeFrame(
            datetime(2022, 1, 1, 10, 20),
            datetime(2022, 1, 1, 10, 50),
        )

        exams = [
            ExamSchedule(
                student=student,
                position=0,
                module=Module(),
                exam_code='exam_1',
                time_frame=first_tf
            ),
            ExamSchedule(
                student=student,
                position=0,
                module=Module(),
                exam_code='exam_2',
                time_frame=second_tf
            ),
            ExamSchedule(
                student=student,
                position=0,
                module=Module(),
                exam_code='exam_3',
                time_frame=third_tf
            ),
        ]

        # ACT
        conflicts = BruteForce.run(student, exams)

        # ASSERT
        assert len(conflicts) == 3

        conflicting_exam_pairs = {
            frozenset(conflict.exams)
            for conflict in conflicts
        }
        expected = {
            frozenset({'exam_1', 'exam_2'}),
            frozenset({'exam_1', 'exam_3'}),
            frozenset({'exam_2', 'exam_3'}),
        }

        assert conflicting_exam_pairs == expected

    @pytest.mark.parametrize('first_tf, second_tf', NON_OVERLAP_TEST_FRAMES)
    def test_feasible_schedule_does_not_produce_conflicts(
            self,
            first_tf,
            second_tf
    ):
        # ARRANGE
        student = Student()

        exams = [
            ExamSchedule(
                student=student,
                position=0,
                module=Module(),
                exam_code='exam_1',
                time_frame=first_tf
            ),
            ExamSchedule(
                student=student,
                position=0,
                module=Module(),
                exam_code='exam_2',
                time_frame=second_tf
            ),
        ]

        # ACT
        conflicts = BruteForce.run(student, exams)

        # ASSERT
        assert not conflicts
