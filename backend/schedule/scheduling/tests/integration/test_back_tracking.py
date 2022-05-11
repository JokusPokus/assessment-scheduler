import pytest


pytestmark = pytest.mark.integration


@pytest.mark.django_db
class TestBackTracking:
    """Test collection for the back-tracking algorithm."""

    pass
