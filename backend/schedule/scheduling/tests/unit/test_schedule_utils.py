import pytest

from datetime import datetime

from schedule.scheduling.schedule import TimeFrame

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
        id='early_first_disjunct'
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
        id='late_first_disjunct'
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
        id='real_overlap_early_first'
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
        id='real_overlap_late_first'
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
        id='back_to_back_early_first'
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
        id='back_to_back_late_first'
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
