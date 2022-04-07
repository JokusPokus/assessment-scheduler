from typing import List

import pandas as pd

from schedule.models import Window
from staff.models import Assessor
from exam.models import Student


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

        self._save_assessors(data.assessor.unique())
        self._save_students(data.student.unique())

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
            assessor.assessment_phases.add(self.window.assessment_phase)

    def _save_students(self, emails: List[Email]) -> None:
        """Save a list of unique email identifiers to the database, each as
        a Student instance.

        :param emails: list of unique emails
        """
        for email in emails:
            student, _ = Student.objects.get_or_create(
                organization=self.organization,
                email=email
            )
