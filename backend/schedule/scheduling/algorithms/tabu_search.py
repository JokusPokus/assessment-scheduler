"""
Implementation of the Tabu Search (TS) meta heuristic.
"""
from abc import ABC, abstractmethod
from collections import deque, UserList
from copy import deepcopy
from datetime import datetime, timedelta
from pprint import pprint
from typing import List, Tuple, Optional
from uuid import uuid4

from .base import BaseAlgorithm
from .random import RandomAssignment
from ..schedule import Schedule, BlockSchedule, ExamSchedule, TimeFrame
from ..types import SlotId
from ..evaluators import Evaluator


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
        schedule.__key = uuid4()

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
        schedule.__key = uuid4()

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


class Neighborhood(ABC, UserList):
    """Defines the neighborhood structure that underlies the search
    problem.

    A neighbor of a schedule is one that can be obtained through one of
    the following operations:

      * Swap a block (A) with another one from a different slot (B)
        whose assessor is also available in A's slot
      * Swap two exams of the same assessor and length
    """

    def __init__(
            self,
            schedule: Schedule,
            actions: Optional[Actions] = None,
            evaluator: Optional[Evaluator] = None
    ):
        super().__init__(self)
        self.schedule = schedule
        self.actions = actions or Actions()
        self.evaluator = evaluator or Evaluator()

        self._set_neighbors()

    @abstractmethod
    def _set_neighbors(self) -> None:
        """Set the self.data attribute with all neighbors of the schedule
        that shall be considered in the search's next iteration.
        """
        pass


class ExamNeighborhood(Neighborhood):
    """Defines the neighborhood of a schedule w.r.t. swapping single exams.

    An exam neighbor of a schedule is obtained by swapping two exams of the
    same assessor, module, and length.
    """

    def _set_neighbors(self) -> None:
        exam_to_swap = self._exam_to_swap()
        exam_to_swap_index = self._get_index_of(exam_to_swap)

        for slot, blocks in self.schedule.items():
            for i, block in enumerate(blocks):
                for j, exam in enumerate(block.exams):
                    if self._swappable(exam, exam_to_swap):
                        exam_indices = [exam_to_swap_index, (slot, i, j)]
                        neighbor = self.actions.swap_exams(
                            self.schedule,
                            exam_indices
                        )
                        self.data.append(neighbor)

    def _exam_to_swap(self) -> ExamSchedule:
        """Return the exam that is to be swapped to get the schedule's
        neighbors.

        The exam is randomly selected from the set of most severely
        punished conflicts of the most-punished student.
        """
        mc_student = self.evaluator.most_conflicted_student(self.schedule)

        conflicts = self.evaluator.conflicts(self.schedule)
        category = self._most_severe_category(conflicts, mc_student)
        mc_exams = conflicts[mc_student][category]

        return random.choice(random.choice(mc_exams).exams)

    @staticmethod
    def _most_severe_category(conflicts, student):
        """Return the most severe degree of conflict that the student
        is involved in.
        """
        return min(conflicts[student].keys())

    @staticmethod
    def _swappable(first: ExamSchedule, second: ExamSchedule) -> bool:
        """Return True if the two exams are swappable according to the
        neighborhood definition.
        """
        return (
            first != second
            and first.student != second.student
            and first.length == second.length
            and first.assessor == second.assessor
            and first.module == second.module
        )

    def _get_index_of(self, exam_to_find: ExamSchedule) -> Tuple[int]:
        """Return the index information to find the given exam schedule
        within the self.schedule.

        The indeces are returned as a tuple (slot_id, block_position,
        exam_position).
        """
        for slot in self.schedule:
            for i, block in enumerate(blocks):
                for j, exam in enumerate(block.exams):
                    if exam == exam_to_find:
                        return slot, i, j


class TabuSearch(BaseAlgorithm):
    """Tabu search is a local meta heuristic that iteratively explores
    the solution space while keeping track of a 'tabu list'.
    """

    def run(self) -> Schedule:
        schedule = RandomAssignment(self.data).run()

        tabu_exam = deque(maxlen=10)

        current_best = [schedule, self.evaluator.penalty(schedule)]

        for _ in range(10):
            for neighbor in ExamNeighborhood(schedule):
                continue

        # Select the best non-tabu one and put the exam on the tabu list.
        # (Unless aspiration criterion met)

        return schedule

    def _iterate(self, schedule: Schedule):
        """Modify the schedule according to the tabu search algorithm, such
        that the resulting schedule is a neighbor of the current one.
        """
        pass
