"""
Assignment of helpers to complete schedules.
"""
from .input_collectors import InputData
from .schedule import Schedule


class HelperAssigner:
    """Randomly assigns available helpers to scheduled exams."""
    def __init__(self, data: InputData):
        self.data = data

    def assign_helpers(self, schedule: Schedule) -> Schedule:
        """Randomly assign helpers to all exams of the given schedule
        and return the enhanced schedule.
        """
        pass
