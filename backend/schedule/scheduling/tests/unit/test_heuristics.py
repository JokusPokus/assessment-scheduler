import pytest

from schedule.scheduling.algorithms.random import SchedulingHeuristics


pytestmark = pytest.mark.unit


class Object(object):
    pass


class TestHeuristics:
    def test_slot_ease_score(self, mocker):
        # GIVEN a slot object that conforms to the specs
        avail_info = Object()
        avail_info.assessor_count = 1
        avail_info.helper_count = 2

        slot = ('some_slot_id', avail_info)

        # THEN the slot ease score is calculated correctly
        expected = (1, 2)
        assert SchedulingHeuristics.slot_ease_score(slot) == expected
