class SheetProcessor:
    """Reads a CSV file and saves the contained information into the
    database, using a normalized schema.
    """

    def __init__(self, file_path: str):
        self.path = file_path

    def populate_db(self) -> None:
        """Read all relevant information from the CSV file located by
        :self.file_path: and save to the appropriate database table.
        """
        pass
