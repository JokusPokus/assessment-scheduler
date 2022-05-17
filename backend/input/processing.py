from typing import List

import pandas as pd
from pandas import DataFrame

from schedule.models import Window
from staff.models import Assessor
from exam.models import Student, Module, Exam, ExamStyle


Email = str


class SheetProcessor:
    """Reads a CSV file and saves the contained information into the
    database, using a normalized schema.

    It is assumed that the CSV file conforms to all expectations stated
    in the validation class <>. Do not use the SheetProcessor before the
    CSV file has been properly validated.
    """

    def __init__(self, window: Window, file_path: str):
        """
        :param window: a Window instance
        :param file_path: the path to a CSV planning sheet
        """
        self.window = window
        self.path = file_path
        self.organization = self.window.assessment_phase.organization

    def populate_db(self) -> None:
        """Read all relevant information from the CSV file located by
        :self.file_path: and save to the appropriate database table.
        """
        data = pd.read_csv(self.path, sep=',')
        module_info = data[['shortCode', 'module']]

        self._save_assessors(data.assessor.unique())
        self._save_students(data.student.unique())
        self._save_modules(module_info.drop_duplicates('shortCode', keep='first'))
        self._save_exams(data)

    def _save_assessors(self, emails: List[Email]) -> None:
        """Save a list of unique email identifiers to the database, each as
        an Assessor instance.

        :param emails: list of unique emails
        """
        for email in emails:
            assessor, _ = Assessor.objects.get_or_create(
                organization=self.organization,
                email=email
            )
            assessor.windows.add(self.window)

    def _save_students(self, emails: List[Email]) -> None:
        """Save a list of unique email identifiers to the database, each as
        a Student instance.

        :param emails: list of unique emails
        """
        for email in emails:
            Student.objects.get_or_create(
                organization=self.organization,
                email=email
            )

    def _save_modules(self, modules: DataFrame) -> None:
        """Save a collection of unique module identifiers and names to the
        database, each as a Module instance.

        :param modules: DataFrame with [unique identifier, name] of modules
        """
        for _, (short_code, name) in modules.iterrows():
            module, _ = Module.objects.get_or_create(
                organization=self.organization,
                code=short_code,
                name=name
            )
            module.windows.add(self.window)

    def _save_exams(self, data: DataFrame) -> None:
        """Save Exam instances based on the CSV data

        :param data: a DataFrame containing exam information
        """
        for _, row in data.iterrows():
            assessor = Assessor.objects.get(email=row['assessor'])
            student = Student.objects.get(email=row['student'])
            module = Module.objects.get(code=row['shortCode'])
            style = {
                'STANDARD': ExamStyle.STANDARD,
                'ALTERNATIVE': ExamStyle.ALTERNATIVE,
                'STS': ExamStyle.STANDARD
            }.get(row['assessmentStyle'])

            if style is None:
                continue

            Exam.objects.get_or_create(
                code=row['assessmentId'],
                window=self.window,
                assessor=assessor,
                student=student,
                module=module,
                style=style
            )
