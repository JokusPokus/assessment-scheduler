import pytest

from schedule.scheduling.algorithms.random import SchedulingHeuristics
from schedule.scheduling.input_collectors import AvailInfo


pytestmark = pytest.mark.unit


class AvailInfoMock:
    def __init__(self, assessor_count, helper_count):
        self.assessor_count = assessor_count
        self.helper_count = helper_count


class AssessorMock:
    pass


class TestHeuristics:
    """Test collection for the heuristic methods that guide the
    back-tracking search.
    """

    def test_slot_ease_score(self):
        # ARRANGE
        avail_info = AvailInfoMock(assessor_count=1, helper_count=2)
        slot = ('some_slot_id', avail_info)

        # ACT
        actual = SchedulingHeuristics.slot_ease_score(slot)

        # ASSERT
        expected = (1, 2)
        assert actual == expected

    def test_assessor_ease_score(self):
        # ARRANGE
        assessor = AssessorMock()
        other_assessor = AssessorMock()

        staff_avails = {
            'slot_1_id': AvailInfo(
                assessor_count=2,
                assessors=[assessor, other_assessor],
                helper_count=1,
                helpers=[object()]
            ),
            'slot_2_id': AvailInfo(
                assessor_count=1,
                assessors=[assessor],
                helper_count=1,
                helpers=[object()]
            ),
            'slot_3_id': AvailInfo(
                assessor_count=1,
                assessors=[other_assessor],
                helper_count=1,
                helpers=[object()]
            ),
        }

        REMAINING_WORKLOAD = 1
        assessor_workload = {
            assessor: {
                'remaining_workload': REMAINING_WORKLOAD
            }
        }

        # ACT
        actual = SchedulingHeuristics.assessor_ease_score(
            assessor,
            staff_avails,
            assessor_workload
        )

        # ASSERT
        assessor_available_blocks = 2
        expected = assessor_available_blocks - REMAINING_WORKLOAD
        assert actual == expected

    def test_assessor_ease_score_with_lack_of_helpers(self):
        # ARRANGE
        assessor = AssessorMock()

        staff_avails = {
            'slot_1_id': AvailInfo(
                assessor_count=1,
                assessors=[assessor],
                helper_count=1,
                helpers=[object()]
            ),
            'slot_2_id': AvailInfo(
                assessor_count=1,
                assessors=[assessor],
                helper_count=0,
                helpers=[]
            ),
        }

        REMAINING_WORKLOAD = 1
        assessor_workload = {
            assessor: {
                'remaining_workload': REMAINING_WORKLOAD
            }
        }

        # ACT
        actual = SchedulingHeuristics.assessor_ease_score(
            assessor,
            staff_avails,
            assessor_workload
        )

        # ASSERT
        assessor_available_blocks = 1
        expected = assessor_available_blocks - REMAINING_WORKLOAD
        assert actual == expected
