"""
Validation of CSV planning sheet.
"""
import io

import pandas as pd
from pandas import DataFrame
from rest_framework.exceptions import ValidationError


class SheetValidator:
    """Validates that all planning sheet requirements are met."""

    REQUIRED_COLS = {
        'assessmentId',
        'student',
        'shortCode',
        'module',
        'assessor',
        'assessmentStyle',
        'assessmentType'
    }

    def __init__(self, file: str):
        self.file = file
        self.errors = {}

    def validate(self) -> None:
        data = pd.read_csv(
            io.StringIO(self.file.read().decode('utf-8')), delimiter=','
        )

        self._collect_validation_errors(data)

        if self.errors:
            raise ValidationError(
                self.errors,
                code='sheet_invalid'
            )

    def _collect_validation_errors(self, data: DataFrame):
        self._validate_contains_required_cols(data)

    def _validate_contains_required_cols(self, data: DataFrame) -> None:
        """Throw validation error if at least one required column is
        not present in the input data.
        """
        missing_cols = self.REQUIRED_COLS - set(data.columns)

        if missing_cols:
            self.errors['missing_cols'] = list(missing_cols)
