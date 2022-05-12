import pytest

from staff.models import Assessor


@pytest.fixture
def assessor_mock():
    class AssessorMock:
        pass

    def make_mock():
        return AssessorMock()

    return make_mock
