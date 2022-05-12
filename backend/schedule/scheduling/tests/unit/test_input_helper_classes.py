import pytest

from schedule.scheduling.input_collectors import AvailInfo, AssessorWorkload
from staff.models import Assessor


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


class TestAssessmentWorkload:
    def test_wrong_key_data_type_throws_error(self):
        # ARRANGE
        workload = AssessorWorkload()

        # ACT / ASSERT
        with pytest.raises(TypeError):
            workload['Not an Assessor instance'] = {}

    def test_decrement_workload_with_valid_data(self):
        # ARRANGE
        assessor = Assessor()
        assessor.pk = 1
        workload = AssessorWorkload()
        workload[assessor] = {
            20: 3,
            30: 5,
        }

        # ACT
        workload.decrement(assessor, 20)

        # ASSERT
        assert workload[assessor][20] == 3 - 1

    def test_decrement_absent_duration_throws_error(self):
        # ARRANGE
        assessor = Assessor()
        assessor.pk = 1
        workload = AssessorWorkload()
        workload[assessor] = {30: 5}

        # ACT / ASSERT
        with pytest.raises(ValueError):
            workload.decrement(assessor, 20)

    def test_decrement_absent_assessor_throws_error(self):
        # ARRANGE
        assessor_1 = Assessor()
        assessor_1.pk = 1
        assessor_2 = Assessor()
        assessor_2.pk = 2

        workload = AssessorWorkload()
        workload[assessor_1] = {30: 5}

        # ACT / ASSERT
        with pytest.raises(ValueError):
            workload.decrement(assessor_2, 30)

    def test_remaining_blocks_calculation(self):
        # ARRANGE
        assessor = Assessor()
        assessor.pk = 1
        workload = AssessorWorkload()
        workload[assessor] = {
            20: 3,
            30: 5,
        }

        # ACT
        actual = workload.remaining_blocks_of(assessor)

        # ASSERT
        assert actual == 3 + 5

    def test_remaining_blocks_of_absent_assessor_throws_error(self):
        # ARRANGE
        assessor_1 = Assessor()
        assessor_1.pk = 1
        assessor_2 = Assessor()
        assessor_2.pk = 2

        workload = AssessorWorkload()
        workload[assessor_1] = {30: 5}

        # ACT / ASSERT
        with pytest.raises(ValueError):
            workload.remaining_blocks_of(assessor_2)
