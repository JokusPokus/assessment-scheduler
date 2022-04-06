import pandas as pd

from ..models import SheetRecord


class DBRecorder:
    """Reads a CSV file and saves the contained information into the
    database, using a normalized schema.
    """

    def __init__(self, file_path: str):
        self.path = file_path

    def write_to_db(self) -> None:
        """Read all relevant information from the CSV file located by
        :self.file_path: and save each line in a separate database record.
        """
