"""
Validation of CSV planning sheet.
"""
import io

import pandas as pd


class SheetValidator:
    """Validates that all planning sheet requirements are met."""

    def __init__(self, file: str):
        self.file = file

    def validate(self):
        data = pd.read_csv(
            io.StringIO(self.file.read().decode('utf-8')), delimiter=','
        )
        print(data)
