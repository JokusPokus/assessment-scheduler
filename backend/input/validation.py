"""
Validation of CSV planning sheet.
"""


class SheetValidator:
    """Validates that all planning sheet requirements are met."""

    def __init__(self, file_path: str):
        self.path = file_path
