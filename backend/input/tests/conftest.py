import os

import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils.timezone import now, timedelta

from user.models import Organization
from schedule.models import AssessmentPhase, Window, Semester, PhaseCategory


@pytest.fixture
def create_phase():
    def make_phase():
        org = Organization.objects.all().get()
        return AssessmentPhase.objects.create(
            organization=org,
            year=2022,
            semester=Semester.SPRING,
            category=PhaseCategory.MAIN
        )

    return make_phase


@pytest.fixture
def create_window(create_phase):
    def make_window():
        return Window.objects.create(
            assessment_phase=create_phase(),
            start_date=now()+timedelta(days=7),
            end_date=now()+timedelta(days=14),
            block_length=180,
        )

    return make_window


@pytest.fixture
def valid_planning_sheet():
    f_dir = os.path.dirname(os.path.abspath(__file__))
    f_name = os.path.join(f_dir, 'files', 'valid_test_sheet.csv')
    with open(f_name, 'rb') as file:
        return SimpleUploadedFile('myPlanningSheet.csv', file.read())
