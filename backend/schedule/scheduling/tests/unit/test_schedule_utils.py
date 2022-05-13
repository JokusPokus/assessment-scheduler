import pytest

from datetime import datetime

from schedule.scheduling.schedule import TimeFrame


pytestmark = pytest.mark.unit


class TestTimeFrame:
    @pytest.mark.parametrize(
        'earlier_frame, later_frame',
        [
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
    )
    def test_time_frame_comparison(self, earlier_frame, later_frame):
        assert earlier_frame < later_frame
