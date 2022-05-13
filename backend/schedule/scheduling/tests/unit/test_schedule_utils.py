import pytest

from datetime import datetime

from exam.models import Exam

from schedule.scheduling.schedule import TimeFrame, BlockSchedule


pytestmark = pytest.mark.unit


TIME_FRAMES = [
    (
        TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 20)
        ),
        TimeFrame(
            datetime(2022, 1, 1, 11, 0),
            datetime(2022, 1, 1, 11, 20)
        )
    ),
    (
        TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 40)
        ),
        TimeFrame(
            datetime(2022, 1, 1, 10, 10),
            datetime(2022, 1, 1, 10, 30)
        )
    ),
]

OVERLAP_TEST_FRAMES = [
    pytest.param(
        TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 20)
        ),
        TimeFrame(
            datetime(2022, 1, 1, 11, 0),
            datetime(2022, 1, 1, 11, 20)
        ),
        False,
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
        False,
        id='late_first__disjunct'
    ),
    pytest.param(
        TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 40)
        ),
        TimeFrame(
            datetime(2022, 1, 1, 10, 10),
            datetime(2022, 1, 1, 10, 30)
        ),
        True,
        id='second_contained_in_first'
    ),
    pytest.param(
        TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 40)
        ),
        TimeFrame(
            datetime(2022, 1, 1, 10, 10),
            datetime(2022, 1, 1, 10, 30)
        ),
        True,
        id='first_contained_in_second'
    ),
    pytest.param(
        TimeFrame(
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 40)
        ),
        TimeFrame(
            datetime(2022, 1, 1, 10, 10),
            datetime(2022, 1, 1, 10, 50)
        ),
        True,
        id='real_overlap__early_first'
    ),
    pytest.param(
        TimeFrame(
            datetime(2022, 1, 1, 10, 20),
            datetime(2022, 1, 1, 10, 40)
        ),
        TimeFrame(
            datetime(2022, 1, 1, 10, 10),
            datetime(2022, 1, 1, 10, 30)
        ),
        True,
        id='real_overlap__late_first'
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
        False,
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
        False,
        id='back_to_back__late_first'
    ),
]


class TestTimeFrame:
    @pytest.mark.parametrize(
        'earlier_frame, later_frame',
        TIME_FRAMES
    )
    def test_time_frame_comparison(self, earlier_frame, later_frame):
        assert earlier_frame < later_frame

    @pytest.mark.parametrize(
        'first_frame, second_frame, expected',
        OVERLAP_TEST_FRAMES
    )
    def test_overlap_is_detected_correctly(
            self,
            first_frame,
            second_frame,
            expected
    ):
        assert first_frame.overlaps_with(second_frame) == expected


class TestBlockSchedule:
    def test_start_times(self, assessor_mock):
        # ARRANGE
        NUM_EXAMS = 3

        block_schedule = BlockSchedule(
            assessor=assessor_mock(),
            start_time=datetime(2022, 1, 1, 10, 0),
            exam_start_times=[0, 20, 80, 100, 120],
            exams=[Exam()] * NUM_EXAMS
        )

        # ACT
        start_times = block_schedule.start_times

        # ASSERT
        assert len(start_times) == NUM_EXAMS
        assert start_times == [
            datetime(2022, 1, 1, 10, 0),
            datetime(2022, 1, 1, 10, 20),
            datetime(2022, 1, 1, 11, 20),
        ]

    def test_start_times_without_block_start_time_throws_error(
            self,
            assessor_mock
    ):
        # ARRANGE
        NUM_EXAMS = 3

        block_schedule = BlockSchedule(
            assessor=assessor_mock(),
            exam_start_times=[0, 20, 80, 100, 120],
            exams=[Exam()] * NUM_EXAMS
        )

        # ACT / ASSERT
        with pytest.raises(AssertionError):
            block_schedule.start_times
