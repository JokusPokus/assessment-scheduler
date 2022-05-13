import pytest

from datetime import datetime

from exam.models import Student, Exam, Module
from staff.models import Assessor

from schedule.scheduling.schedule import (
    Schedule,
    BlockSchedule,
    ExamSchedule,
    TimeFrame,
)

pytestmark = pytest.mark.unit


class TestSchedule:
    def test_group_by_student(self):
        # ARRANGE
        schedule = Schedule()

        student_1 = Student(id=1)
        student_2 = Student(id=2)

        students = [student_1, student_2]

        for i in range(2):
            exams = [
                ExamSchedule(
                    exam_code=f'block_{i}_student_{student.id}',
                    module=Module(),
                    position=j,
                    student=student,
                    time_frame=TimeFrame(
                        datetime(2022, 1, 1, 10, 0),
                        datetime(2022, 1, 1, 10, 20)
                    )
                )
                for j, student in enumerate(students)
            ]

            schedule[i] += [
                BlockSchedule(
                    assessor=Assessor(),
                    exams=exams
                )
            ]

        # ACT
        by_student = schedule.group_by_student()

        # ASSERT
        assert len(by_student) == 2

        s1_exams = by_student[student_1]
        expected_codes = {'block_0_student_1', 'block_1_student_1'}
        assert {exam.exam_code for exam in s1_exams} == expected_codes

        s2_exams = by_student[student_2]
        expected_codes = {'block_0_student_2', 'block_1_student_2'}
        assert {exam.exam_code for exam in s2_exams} == expected_codes

    def test_num_total_blocks(self):
        # ARRANGE
        ass = Assessor()

        schedule = Schedule()
        schedule[1] = [BlockSchedule(assessor=ass)] * 3
        schedule[2] = []
        schedule[3] = [BlockSchedule(assessor=ass)] * 5

        # ACT / ASSERT
        assert schedule.total_blocks_scheduled == 3 + 5
