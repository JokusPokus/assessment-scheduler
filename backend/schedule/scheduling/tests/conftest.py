import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from django.utils.timezone import now

from exam.models import Exam, Module, Student, ExamStyle
from staff.models import Assessor
from user.models import Organization
from schedule.models import (
    AssessmentPhase,
    Window,
    BlockSlot,
    BlockTemplate,
    Semester,
    PhaseCategory
)


@pytest.fixture
def assessor_mock():
    class AssessorMock:
        pass

    def make_mock():
        return AssessorMock()

    return make_mock


@pytest.fixture
def create_window():
    def make_window(**kwargs):
        phase, _ = AssessmentPhase.objects.get_or_create(
            year=2022,
            semester=Semester.SPRING,
            category=PhaseCategory.MAIN,
            organization=Organization.objects.all().first(),
        )
        attrs = {
            'assessment_phase': phase,
            'start_date': now().date(),
            'end_date': now().date() + timedelta(days=5),
            'block_length': 180,
            **kwargs
        }
        window = Window.objects.create(**attrs)
        window.block_templates.add(
            BlockTemplate.objects.get(exam_length=20),
            BlockTemplate.objects.get(exam_length=30),
        )
        return window

    return make_window


@pytest.fixture
def create_assessor(create_window):
    def make_assessor(**kwargs):
        if 'window' in kwargs:
            window = kwargs.pop('window')
        else:
            window = create_window()
        attrs = {
            'email': f'assessor{str(uuid4())[:6]}@code.berlin',
            'organization': Organization.objects.all().first(),
            **kwargs
        }
        assessor = Assessor.objects.create(**attrs)
        assessor.windows.add(window)
        return assessor
    return make_assessor


@pytest.fixture
def create_student():
    def make_student(**kwargs):
        attrs = {
            'email': f'student{str(uuid4())[:6]}@code.berlin',
            'organization': Organization.objects.all().first(),
            **kwargs
        }
        return Student.objects.create(**attrs)
    return make_student


@pytest.fixture
def create_modules(create_window):
    def make_modules(n: int = 1, **kwargs):
        modules = []
        if 'window' in kwargs:
            window = kwargs.pop('window')
        else:
            window = create_window()

        for _ in range(n):
            attrs = {
                'name': str(uuid4())[:8],
                'code': str(uuid4())[:8],
                'organization': Organization.objects.all().first(),
                'standard_length': 20,
                'alternative_length': 30,
                'created': now(),
                'modified': now(),
                **kwargs
            }
            modules.append(Module(**attrs))
        modules = Module.objects.bulk_create(modules)
        for module in modules:
            module.windows.add(window)
        return modules if len(modules) > 1 else modules[0]
    return make_modules


@pytest.fixture
def create_exams(create_window, create_student, create_assessor, create_modules):
    def make_exams(n: int = 1, **kwargs):
        exams = []
        if 'window' in kwargs:
            window = kwargs.pop('window')
        else:
            window = create_window()

        for _ in range(n):
            attrs = {
                'code': str(uuid4())[:8],
                'student': kwargs.get('student') or create_student(),
                'window': window,
                'module': kwargs.get('module') or create_modules(n=1, window=window),
                'style': ExamStyle.STANDARD,
                'assessor': kwargs.get('assessor') or create_assessor(),
                'created': now(),
                'modified': now(),
                **kwargs
            }
            exams.append(Exam(**attrs))
        return Exam.objects.bulk_create(exams)
    return make_exams


@pytest.fixture
def workload_calc_mock():
    class CalcMock:
        assessor_block_counts = {}

    return CalcMock()
