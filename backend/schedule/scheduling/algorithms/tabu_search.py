"""
Implementation of the Tabu Search (TS) meta heuristic.
"""
from collections import deque
from copy import deepcopy
from datetime import datetime, timedelta
from pprint import pprint
from typing import List, Tuple

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
            block_indeces: List[Tuple[SlotId, int]]
    ) -> Schedule:
        """Swap the given blocks and return a modified
        copy of the schedule.
        """
        schedule = deepcopy(schedule)

        first, second = self._pop_blocks(schedule, block_indeces)
        self._swap_start_times(first, second)

        for block in [first, second]:
            self._update_exam_time_frames_of(block)

        self._add_updated_blocks(schedule, first, second, block_indeces)
        return schedule

    def swap_exams(
            self,
            schedule: Schedule,
            exam_indices: List[Tuple[SlotId, int, int]]
    ):
        """Swap the given exams and return a modified
        copy of the schedule.
        """
        schedule = deepcopy(schedule)

        first, second = self._get_exams(schedule, exam_indices)
        self._swap_attributes(first, second)

        return schedule

    @staticmethod
    def _pop_blocks(
            schedule: Schedule,
            block_indices: List[Tuple[SlotId, int]]
    ) -> Tuple[BlockSchedule]:
        """Pop the blocks from the schedule and return them."""
        (slot_id_1, first_id), (slot_id_2, second_id) = block_indices

        first = schedule[slot_id_1].pop(first_id)
        second = schedule[slot_id_2].pop(second_id)

        return first, second

    @staticmethod
    def _swap_start_times(first: BlockSchedule, second: BlockSchedule) -> None:
        """Swap the start times of the two blocks."""
        first.start_time, second.start_time = second.start_time, first.start_time

    @staticmethod
    def _update_exam_time_frames_of(block: BlockSchedule) -> None:
        """Update the exams' time frames according to the new start times."""
        if len(block.exam_start_times) < len(block.exams):
            raise ValueError('Not enough exam start times given for this block')

        for exam, start_time in zip(block.exams, block.start_times):
            exam.time_frame.start_time = start_time
            exam.time_frame.end_time = start_time + block.delta

    @staticmethod
    def _add_updated_blocks(
            schedule: Schedule,
            first: BlockSchedule,
            second: BlockSchedule,
            block_indices: List[Tuple[SlotId, int]]
    ) -> None:
        """Add the updated blocks to the schedule."""
        (slot_id_1, _), (slot_id_2, _) = block_indices

        schedule[slot_id_1].append(second)
        schedule[slot_id_2].append(first)

    @staticmethod
    def _get_exams(
            schedule: Schedule,
            exam_indices: List[Tuple[SlotId, int, int]]
    ) -> Tuple[ExamSchedule]:
        """Return the two exam schedules corresponding to the given
        indices.
        """
        (slot_1, block_1, exam_1), (slot_2, block_2, exam_2) = exam_indices
        first = schedule[slot_1][block_1].exams[exam_1]
        second = schedule[slot_2][block_2].exams[exam_2]
        return first, second

    @staticmethod
    def _swap_attributes(first: ExamSchedule, second: ExamSchedule) -> None:
        """Swap the dynamic attributes that change when two exams
        are swapped.

        The position and time frame remain the same.
        """
        first.exam_code, second.exam_code = second.exam_code, first.exam_code
        first.student, second.student = second.student, first.student
        first.module, second.module = second.module, first.module


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

        pprint(self.evaluator.conflicts(schedule))
        print("UTILITY:", self.evaluator.utility(schedule))

        return schedule

    def _iterate(self, schedule: Schedule):
        """Modify the schedule according to the tabu search algorithm, such
        that the resulting schedule is a neighbor of the current one.
        """
        pass
