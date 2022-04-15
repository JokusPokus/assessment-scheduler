import os

import pytest

from django.urls import reverse


pytestmark = pytest.mark.acceptance


@pytest.mark.django_db
class TestSheetValidation:
    def test_valid_sheet_passes_validation(
            self,
            authenticated_client,
            create_window,
            valid_planning_sheet
    ):
        # GIVEN a window instance and a valid CSV planning sheet
        window = create_window()
        sheet = valid_planning_sheet

        # WHEN the sheet is uploaded via the API
        response = authenticated_client.post(
            path=reverse('sheet_upload', args=['myPlanningSheet.csv']),
            data={'csv': sheet, 'window': window.id},
            format='multipart'
        )

        # THEN the sheet is accepted and no validation error is raised
        assert response.status_code == 200
