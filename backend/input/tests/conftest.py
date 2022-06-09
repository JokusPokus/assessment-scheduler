import os

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils.timezone import now, timedelta

from user.models import Organization
from schedule.models import AssessmentPhase, Window, Semester, PhaseCategory


@pytest.fixture
def default_phase():
    org = Organization.objects.all().get()
    return AssessmentPhase.objects.get(
        organization=org,
        year=2022,
        semester=Semester.SPRING,
        category=PhaseCategory.MAIN
    )


@pytest.fixture
def create_window(default_phase):
    def make_window():
        return Window.objects.create(
            assessment_phase=default_phase,
            start_date=now()+timedelta(days=7),
            end_date=now()+timedelta(days=14),
            block_length=180,
        )

    return make_window


@pytest.fixture
def create_sheet():
    def make_sheet(csv_name):
        f_dir = os.path.dirname(os.path.abspath(__file__))
        f_name = os.path.join(f_dir, 'files', csv_name)
        with open(f_name, 'rb') as file:
            return SimpleUploadedFile('myPlanningSheet.csv', file.read())

    return make_sheet


@pytest.fixture
def valid_planning_sheet(create_sheet):
    return create_sheet('valid_planning_sheet.csv')


@pytest.fixture
def planning_sheet_w_missing_col(create_sheet):
    return create_sheet('planning_sheet_w_missing_col.csv')


@pytest.fixture
def planning_sheet_with_non_email_student(create_sheet):
    return create_sheet('planning_sheet_with_non_email_student.csv')
