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

CONFLICT_CATEGORIES_TEST_DATA = [
    pytest.param(
        TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 20)
        ),
        TimeFrame(
            datetime(2022, 1, 1, 10, 10),
            datetime(2022, 1, 1, 10, 30)
        ),
        'first_order',
        id='first_order'
    ),
    pytest.param(
        TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 20)
        ),
        TimeFrame(
            datetime(2022, 1, 1, 13, 10),
            datetime(2022, 1, 1, 13, 40)
        ),
        'shortly_followed',
        id='shortly_followed'
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
        'shortly_followed',
        id='back_to_back'
    ),
    pytest.param(
        TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 20)
        ),
        TimeFrame(
            datetime(2022, 1, 1, 13, 20),
            datetime(2022, 1, 1, 13, 40)
        ),
        'same_day',
        id='same_day_minimal_break'
    ),
    pytest.param(
        TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 20)
        ),
        TimeFrame(
            datetime(2022, 1, 2, 10, 10),
            datetime(2022, 1, 2, 10, 30)
        ),
        'consecutive_days',
        id='consecutive_days'
    ),
]


class TestBruteForceAlgorithm:
    @pytest.mark.parametrize(
        'first_tf, second_tf, conflict_category',
        CONFLICT_CATEGORIES_TEST_DATA
    )
    def test_existing_conflict_is_assigned_correct_category(
            self,
            first_tf,
            second_tf,
            conflict_category
    ):
        # ARRANGE
        student = Student(id=1)

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
        conflicts = BruteForce().run({student: exams})

        # ASSERT
        assert len(conflicts[conflict_category]) == 1

        categories = [
            'first_order',
            'shortly_followed',
            'same_day',
            'consecutive_days'
        ]
        categories.remove(conflict_category)
        for cat in categories:
            assert not conflicts[cat]

        conflict = conflicts[conflict_category][0]
        assert isinstance(conflict, Conflict)
        assert conflict.student == student
        assert set(conflict.exams) == {'exam_1', 'exam_2'}

    def test_conflicts_are_recorded_pairwise(self):
        # ARRANGE
        student = Student(id=1)

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
        conflicts = BruteForce().run({student: exams})

        # ASSERT
        assert len(conflicts['first_order']) == 3

        conflicting_exam_pairs = {
            frozenset(conflict.exams)
            for conflict in conflicts['first_order']
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
        student = Student(id=1)

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
        conflicts = BruteForce().run({student: exams})

        # ASSERT
        assert not conflicts['first_order']
