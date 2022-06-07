"""
Assignment of helpers to complete schedules.
"""
from copy import deepcopy
from random import randint

from .input_collectors import InputData
from .schedule import Schedule


class HelperAssigner:
    """Randomly assigns available helpers to scheduled exams."""

    @staticmethod
    def assign_helpers(schedule: Schedule, data: InputData) -> Schedule:
        """Randomly assign helpers to all exams of the given schedule
        and return the enhanced schedule.
        """
        staff_avails = deepcopy(data.staff_avails)

        for slot, blocks in schedule.items():
            for block in blocks:
                helpers = staff_avails[slot].helpers
                rand_index = randint(0, len(helpers) - 1)
                block.helper = helpers.pop(rand_index)

        return schedule
