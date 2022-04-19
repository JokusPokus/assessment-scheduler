import os

import pytest

from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


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
        assert response.status_code == HTTP_200_OK

    def test_sheet_with_missing_column_fails_validation(
            self,
            authenticated_client,
            create_window,
            planning_sheet_w_missing_col
    ):
        # GIVEN a window instance and a CSV planning sheet with a required
        # column missing
        window = create_window()
        sheet = planning_sheet_w_missing_col

        # WHEN the sheet is uploaded via the API
        response = authenticated_client.post(
            path=reverse('sheet_upload', args=['myPlanningSheet.csv']),
            data={'csv': sheet, 'window': window.id},
            format='multipart'
        )

        # THEN the sheet is rejected with the missing column name in the
        # error response
        assert response.status_code == HTTP_400_BAD_REQUEST

        expected_errors = {'missing_cols': ['assessmentType']}
        assert response.json().get('csv') == expected_errors

    def test_sheet_with_bad_email_format_fails_validation(
            self,
            authenticated_client,
            create_window,
            planning_sheet_with_non_email_student
    ):
        # GIVEN a window instance and a CSV planning sheet with a student
        # whose identifier is not a CODE email address
        window = create_window()
        sheet = planning_sheet_with_non_email_student

        # WHEN the sheet is uploaded via the API
        response = authenticated_client.post(
            path=reverse('sheet_upload', args=['myPlanningSheet.csv']),
            data={'csv': sheet, 'window': window.id},
            format='multipart'
        )

        # THEN the sheet is rejected with the hint that the student column
        # contains a non-email identifier
        assert response.status_code == HTTP_400_BAD_REQUEST

        expected_errors = {'wrong_email_format': ['student']}
        assert response.json().get('csv') == expected_errors
