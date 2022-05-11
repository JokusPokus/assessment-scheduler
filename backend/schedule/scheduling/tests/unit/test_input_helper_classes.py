import pytest

from schedule.scheduling.input_collectors import AvailInfo, AssessorWorkload


pytestmark = pytest.mark.unit


class TestAvailInfo:
    def test_remove_assessor_from_avail_info(self, assessor_mock):
        # ARRANGE
        assessor_1 = assessor_mock()
        assessor_2 = assessor_mock()

        avail_info = AvailInfo(
            assessor_count=2,
            assessors=[assessor_1, assessor_2],
            helper_count=0,
            helpers=[]
        )

        # ACT
        avail_info.remove(assessor_1)

        # ASSERT
        assert avail_info.assessor_count == 1
        assert avail_info.assessors == [assessor_2]

    def test_removing_non_existing_assessor_throws_error(self, assessor_mock):
        # ARRANGE
        assessor_1 = assessor_mock()
        assessor_2 = assessor_mock()

        avail_info = AvailInfo(
            assessor_count=1,
            assessors=[assessor_1],
            helper_count=0,
            helpers=[]
        )

        # ACT / ASSERT
        with pytest.raises(ValueError):
            avail_info.remove(assessor_2)
