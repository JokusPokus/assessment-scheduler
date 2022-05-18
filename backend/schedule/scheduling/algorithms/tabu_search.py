"""
Implementation of the Tabu Search (TS) meta heuristic.
"""
from collections import deque
from copy import deepcopy
from datetime import datetime, timedelta
from typing import List

from .base import BaseAlgorithm
from .random import RandomAssignment
from ..schedule import Schedule, BlockSchedule, ExamSchedule, TimeFrame
from ..types import SlotId


class Actions:
    """Implements the actions that correspond to a single step through
    the optimization problem's search space.
    """

    def swap_blocks(
            self,
            schedule: Schedule,
            blocks: List[Tuple[SlotId, BlockSchedule]]
    ) -> Schedule:
        """Swap the given blocks and return a modified
        copy of the schedule.
        """
        schedule = deepcopy(schedule)
        (slot_id_1, first), (slot_id_2, second) = deepcopy(blocks)

        self._remove_blocks(schedule, first, second, slot_id_1, slot_id_2)
        self._swap_start_times(first, second)

        for block in [first, second]:
            self._update_exam_time_frames_of(block)

        self._add_updated_blocks(schedule, first, second, slot_id_1, slot_id_2)
        return schedule

    @staticmethod
    def _remove_blocks(
            schedule: Schedule,
            first: BlockSchedule,
            second: BlockSchedule,
            slot_id_1: SlotId,
            slot_id_2: SlotId
    ) -> None:
        """Remove the blocks from the schedule."""
        schedule[slot_id_1].remove(first)
        schedule[slot_id_2].remove(second)

    @staticmethod
    def _swap_start_times(first: BlockSchedule, second: BlockSchedule) -> None:
        """Swap the start times of the two blocks."""
        first.start_time, second.start_time = second.start_time, first.start_time

    @staticmethod
    def _update_exam_time_frames_of(block: BlockSchedule) -> None:
        """Update the exams' time frames according to the new start times."""
        for exam, start_time in zip(block.exams, block.start_times):
            exam.time_frame.start_time = start_time
            exam.time_frame.end_time = start_time + block.delta

    @staticmethod
    def _add_updated_blocks(
            schedule: Schedule,
            first: BlockSchedule,
            second: BlockSchedule,
            slot_id_1: SlotId,
            slot_id_2: SlotId
    ) -> None:
        """Add the updated blocks to the schedule."""
        schedule[slot_id_1].append(second)
        schedule[slot_id_2].append(first)


class Neighborhood:
    """Defines the neighborhood structure that underlies the search
    problem.

    A neighbor of a schedule is one that can be obtained through one of
    the following operations:

      * Swap a block (A) with another one from a different slot (B)
        whose assessor is also available in A's slot
      * Swap two exams of the same assessor and length
    """
    pass


class TabuSearch(BaseAlgorithm):
    """Tabu search is a local meta heuristic that iteratively explores
    the solution space while keeping track of a 'tabu list'.
    """

    def run(self) -> Schedule:
        schedule = RandomAssignment(self.data).run()

        print(self.evaluator.utility(schedule))

        return schedule

    def _iterate(self, schedule: Schedule):
        """Modify the schedule according to the tabu search algorithm, such
        that the resulting schedule is a neighbor of the current one.
        """
        pass
