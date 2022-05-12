import pytest

import math

from exam.models import ExamStyle, Exam
from schedule.models import BlockTemplate
from staff.models import Assessor

from schedule.scheduling.input_collectors import WorkloadCalculator


pytestmark = pytest.mark.integration


@pytest.mark.django_db
class TestWorkloadCalculator:
    def test_calculate_assessor_block_counts(
            self,
            create_assessor,
            create_modules,
            create_exams,
            create_window,
    ):
        # ARRANGE
        window = create_window()
        ass = create_assessor(window=window)

        module_20_30 = create_modules(
            n=1,
            standard_length=20,
            alternative_length=30
        )
        module_30_20 = create_modules(
            n=1,
            standard_length=30,
            alternative_length=20
        )

        create_exams(
            n=6,
            style=ExamStyle.STANDARD,
            assessor=ass,
            module=module_20_30,
        )
        create_exams(
            n=4,
            style=ExamStyle.ALTERNATIVE,
            assessor=ass,
            module=module_20_30,
        )
        create_exams(
            n=5,
            style=ExamStyle.STANDARD,
            assessor=ass,
            module=module_30_20,
        )
        create_exams(
            n=1,
            style=ExamStyle.ALTERNATIVE,
            assessor=ass,
            module=module_30_20,
        )

        calc = WorkloadCalculator(
            assessors=Assessor.objects.filter(id=ass.id),
            exams=Exam.objects.filter(assessor=ass),
            block_templates=BlockTemplate.objects.filter(
                exam_length__in=[20, 30]
            ),
        )

        # ACT
        workload = calc.assessor_block_counts

        # ASSERT
        expected_exams_20 = 6 + 1
        num_exams_per_block_20 = len(
            BlockTemplate.objects.get(exam_length=20).exam_start_times
        )

        expected_exams_30 = 4 + 5
        num_exams_per_block_30 = len(
            BlockTemplate.objects.get(exam_length=30).exam_start_times
        )

        expected = {
            20: math.ceil(expected_exams_20 / num_exams_per_block_20),
            30: math.ceil(expected_exams_30 / num_exams_per_block_30)
        }

        assert workload == {ass: expected}

    def test_other_assessors_do_not_interfere(
            self,
            create_assessor,
            create_modules,
            create_exams,
            create_window,
    ):
        # ARRANGE
        window = create_window()
        ass = create_assessor(window=window)
        other_ass = create_assessor(window=window)

        module_20_30 = create_modules(
            n=1,
            standard_length=20,
            alternative_length=30
        )

        create_exams(
            n=7,
            style=ExamStyle.STANDARD,
            assessor=ass,
            module=module_20_30,
        )
        create_exams(
            n=7,
            style=ExamStyle.STANDARD,
            assessor=other_ass,
            module=module_20_30,
        )

        calc = WorkloadCalculator(
            assessors=Assessor.objects.filter(id__in=[ass.id, other_ass.id]),
            exams=Exam.objects.filter(assessor__in=[ass.id, other_ass.id]),
            block_templates=BlockTemplate.objects.filter(
                exam_length__in=[20, 30]
            ),
        )

        # ACT
        workload = calc.assessor_block_counts

        # ASSERT
        expected_exams_20 = 7
        num_exams_per_block_20 = len(
            BlockTemplate.objects.get(exam_length=20).exam_start_times
        )

        assert len(workload) == 2
        assert workload[ass] == {
            20: math.ceil(expected_exams_20 / num_exams_per_block_20)
        }
