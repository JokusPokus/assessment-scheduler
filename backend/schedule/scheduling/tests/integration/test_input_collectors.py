import pytest
from pytest_django.asserts import assertQuerysetEqual

from exam.models import ExamStyle, Exam, Module
from schedule.models import BlockTemplate
from staff.models import Assessor

from schedule.scheduling.input_collectors import DBInputCollector


pytestmark = pytest.mark.integration


@pytest.mark.django_db
class TestDBInputCollector:
    def test_input_is_read_correctly(
            self,
            workload_calc_mock,
            create_window,
            create_assessor,
            create_modules,
            create_exams
    ):
        # ARRANGE
        window = create_window()
        other_window = create_window()

        related_ass = create_assessor(window=window)
        unrelated_ass = create_assessor(window=other_window)

        related_module = create_modules(window=window)
        unrelated_module = create_modules(window=other_window)

        related_exams = create_exams(
            n=3,
            style=ExamStyle.STANDARD,
            assessor=related_ass,
            module=related_module,
            window=window
        )
        unrelated_exams = create_exams(
            n=3,
            style=ExamStyle.STANDARD,
            assessor=related_ass,
            module=related_module,
            window=other_window
        )

        collector = DBInputCollector(
            window,
            workload_calculator=workload_calc_mock
        )

        # ACT
        data = collector.collect()

        # ASSERT
        assertQuerysetEqual(
            data.assessors,
            Assessor.objects.filter(id=related_ass.id)
        )
        assertQuerysetEqual(
            data.modules,
            Module.objects.filter(id=related_module.id)
        )
        assert {exam.id for exam in data.exams} \
               == {exam.id for exam in related_exams}
        assert {temp.id for temp in data.block_templates} \
               == {temp.id for temp in BlockTemplate.objects.all()}
