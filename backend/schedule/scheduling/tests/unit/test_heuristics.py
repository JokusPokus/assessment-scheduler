import pytest

from schedule.scheduling.algorithms.random import SchedulingHeuristics


pytestmark = pytest.mark.unit


class AvailInfoMock:
    def __init__(self, assessor_count, helper_count):
        self.assessor_count = assessor_count
        self.helper_count = helper_count


class TestHeuristics:
    def test_slot_ease_score(self, mocker):
        # GIVEN a slot object that conforms to the specs
        avail_info = AvailInfoMock(assessor_count=1, helper_count=2)
        slot = ('some_slot_id', avail_info)

        # THEN the slot ease score is calculated correctly
        expected = (1, 2)
        assert SchedulingHeuristics.slot_ease_score(slot) == expected
