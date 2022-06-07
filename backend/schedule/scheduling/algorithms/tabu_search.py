"""
Implementation of the Tabu Search (TS) meta heuristic.
"""
from abc import ABC, abstractmethod
from collections import deque, UserList, defaultdict
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timedelta
import math
from pprint import pprint
import random
from timeit import default_timer
from typing import List, Tuple, Optional
from uuid import uuid4

from django.conf import settings

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
        schedule._key = uuid4()

        first, second = self._pop_blocks(schedule, block_indeces)
        self._swap_start_times(first, second)

        for block in [first, second]:
            self._update_exams_of(block)

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

        # Needed to make schedules hashable for function call caching
        schedule._key = uuid4()

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
    def _update_exams_of(block: BlockSchedule) -> None:
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
        first.block, second.block = second.block, first.block


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
        that shall be considered in the next search iteration.
        """
        pass


class ExamNeighborhood(Neighborhood):
    """Defines the neighborhood of a schedule w.r.t. swapping single exams.

    An exam neighbor of a schedule is obtained by swapping two exams of the
    same assessor, module and length.
    """

    def _set_neighbors(self) -> None:
        exam_to_swap = self._exam_to_swap()
        exam_to_swap_index = self._get_index_of(exam_to_swap)

        for slot, blocks in self.schedule.items():
            for i, block in enumerate(blocks):
                if not self._compatible_lengths(block, exam_to_swap):
                    continue

                for j, exam in enumerate(block.exams):
                    if self._swappable(exam, exam_to_swap):

                        exam_indices = [exam_to_swap_index, (slot, i, j)]
                        neighbor = self.actions.swap_exams(
                            self.schedule,
                            exam_indices
                        )

                        neighbor.swapped_exam = exam
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
    def _compatible_lengths(block: BlockSchedule, exam: ExamSchedule) -> bool:
        """Return True if the block's exam length is the same as the
        exam's length.
        """
        return block.exam_length == exam.time_frame.length(as_int=True)

    @staticmethod
    def _swappable(first: ExamSchedule, second: ExamSchedule) -> bool:
        """Return True if the two exams are swappable according to the
        neighborhood definition.
        """
        return (
            first != second
            and first.student != second.student
            and first.assessor == second.assessor
            and first.module == second.module
        )

    def _get_index_of(self, exam_to_find: ExamSchedule) -> Tuple[int]:
        """Return the index information to find the given exam schedule
        within the self.schedule.

        The indeces are returned as a tuple (slot_id, block_position,
        exam_position).
        """
        for slot, blocks in self.schedule.items():
            for i, block in enumerate(blocks):
                for j, exam in enumerate(block.exams):
                    if exam == exam_to_find:
                        return slot, i, j


class BlockNeighborhood(Neighborhood):
    """Defines the neighborhood of a schedule w.r.t. swapping entire blocks.

    A block neighbor of a schedule is obtained by swapping two blocks of
    the same assessor.
    """
    MAX_NEIGHBORS = 5

    def _set_neighbors(self) -> None:
        block_to_swap = self.evaluator.most_conflicted_block(self.schedule)
        block_to_swap_index = self._get_index_of(block_to_swap)

        for slot, blocks in self.schedule.items():
            for i, block in enumerate(blocks):
                if self._swappable(block, block_to_swap):
                    block_indices = [block_to_swap_index, (slot, i)]
                    neighbor = self.actions.swap_blocks(
                        self.schedule,
                        block_indices
                    )
                    neighbor.swapped_block = block
                    self.data.append(neighbor)

                    if len(self.data) > self.MAX_NEIGHBORS:
                        return

    def _get_index_of(self, block_to_find: BlockSchedule) -> Tuple[int]:
        """Return the index information to find the given block schedule
        within the self.schedule.

        The indeces are returned as a tuple (slot_id, block_position).
        """
        for slot, blocks in self.schedule.items():
            try:
                index = blocks.index(block_to_find)
            except ValueError:
                pass
            else:
                return slot, index

    @staticmethod
    def _swappable(first: BlockSchedule, second: BlockSchedule) -> bool:
        """Return True if the two blocks are swappable according to the
        neighborhood definition.
        """
        return first != second and first.assessor == second.assessor


class SearchContext(ABC):
    """Keeps track of and processes context metrics
    that help guide the search algorithm.
    """
    MAX_ITERATIONS_WITHOUT_IMPROVEMENT = None

    def __init__(self, initial: Schedule):
        self.initial = initial
        self.iterations_since_improvement = 0
        self.improved = True

    def termination_criterion_met(self) -> bool:
        """Return True if the the last number of iterations has not
        produced a penalty improvement.

        The concrete number is given as a parameter.
        """
        if not self.improved:
            self.iterations_since_improvement += 1

            if self.iterations_since_improvement \
                    > self.MAX_ITERATIONS_WITHOUT_IMPROVEMENT:
                return True

        else:
            self.iterations_since_improvement = 0

        return False

    @abstractmethod
    def initialize_iteration(self) -> None:
        """Refresh the context for a new iteration of neighborhood search."""
        pass

    def record_improvement(self) -> None:
        self.improved = True


class BlockSearchContext(SearchContext):
    MAX_ITERATIONS_WITHOUT_IMPROVEMENT = 2

    def __init__(self, initial: Schedule):
        super().__init__(initial)
        self.best_penalties_of_block_neighbors = {
            initial: Evaluator().penalty(initial)
        }

    def ranked_block_neighbors_of_previous_iteration(self):
        """Return the block neighbors found in the last block
        neighborhood iteration, ranked by its optimal penalties.
        """
        return sorted(
            self.best_penalties_of_block_neighbors.items(),
            key=lambda x: x[1]
        )

    def initialize_iteration(self) -> None:
        """Refresh the context for a new iteration of
        block neighborhood search.
        """
        self.improved = False
        self.best_penalties_of_block_neighbors = defaultdict(lambda: math.inf)

    def record(
            self,
            neighbor: Schedule,
            relative_best: int,
    ) -> None:
        """Record the best score that was achieved during the search
        process starting form the given block.
        """
        self.best_penalties_of_block_neighbors[neighbor] = relative_best


class ExamSearchContext(SearchContext):
    MAX_ITERATIONS_WITHOUT_IMPROVEMENT = 10

    def initialize_iteration(self) -> None:
        self.improved = False


class TabuList:
    def __init__(self, max_len: int):
        self.records = deque(maxlen=max_len)

    def __contains__(self, item):
        assert hasattr(item, 'exam_code'), 'The tabu list contains exams only'
        return item.exam_code in self.records

    def add(self, item) -> None:
        assert hasattr(item, 'exam_code'), 'The tabu list contains exams only'
        self.records.append(item.exam_code)


class Logger:
    def __init__(self, verbose: Optional[bool] = None):
        self.log = print if verbose else self._shut_up
        self.brag = self._brag if verbose else self._shut_up

        if verbose is None:
            verbose = settings.APPLICATION_STAGE == 'development'
        self.verbose = verbose

    @staticmethod
    def _shut_up(*args, **kwargs):
        pass

    @staticmethod
    def _brag(final_penalty, start_time) -> None:
        end_time = default_timer()
        total_time = int(end_time - start_time)

        print("\n*")
        print("**")
        print("****")
        print("********")
        print(f"Best solution found in {total_time}s: {final_penalty}")
        print("********")
        print("****")
        print("**")
        print("*")


class TabuSearch(BaseAlgorithm):
    """Tabu search is a local meta heuristic that iteratively explores
    the solution space while keeping track of a 'tabu list'.
    """

    def run(self, verbose=False) -> Tuple[Schedule, int]:
        logger = Logger(verbose=verbose)
        start_time = default_timer()

        tabu_exams = TabuList(max_len=8)

        # Initialize search context
        current_solution = self._get_initial_solution()

        absolute_best = [
            current_solution,
            self.evaluator.penalty(current_solution)
        ]

        if absolute_best[1] == 0:
            logger.brag(0, start_time)
            return current_solution, 0

        block_context = BlockSearchContext(current_solution)

        while True:
            if block_context.termination_criterion_met():
                break

            ranked_neighbors \
                = block_context.ranked_block_neighbors_of_previous_iteration()

            for potential, _ in ranked_neighbors:
                block_neighborhood = BlockNeighborhood(potential)
                if block_neighborhood:
                    break
                logger.log("(Skipped solution without neighbors)")
            else:
                logger.brag(absolute_best[1], start_time)
                return tuple(absolute_best)

            logger.log("\n******\nNEW BLOCK SEARCH\n******")

            block_context.initialize_iteration()

            for block_neighbor in block_neighborhood:
                exam_context = ExamSearchContext(block_neighbor)

                # Initialize exam search for the block neighbor
                current_solution = block_neighbor
                relative_best = [
                    block_neighbor,
                    self.evaluator.penalty(block_neighbor)
                ]

                if relative_best[1] == 0:
                    logger.brag(0, start_time)
                    return current_solution, 0

                logger.log(f"\nNEW BLOCK NEIGHBOR: {relative_best[1]}\n")

                while True:
                    if exam_context.termination_criterion_met():
                        best_schedule, best_penalty = relative_best
                        block_context.record(best_schedule, best_penalty)
                        break

                    exam_context.initialize_iteration()

                    scored_exam_neighbors = self._get_scored_exam_neighbors_of(
                        current_solution
                    )

                    for exam_neighbor, penalty in scored_exam_neighbors:
                        if penalty == 0:
                            logger.brag(0, start_time)
                            return exam_neighbor, 0

                        not_tabu = exam_neighbor.swapped_exam not in tabu_exams
                        aspiration_criterion_met = penalty < absolute_best[1]

                        if not_tabu or aspiration_criterion_met:
                            current_solution = exam_neighbor
                            tabu_exams.add(exam_neighbor.swapped_exam)

                            is_relative_improvement \
                                = penalty < relative_best[1]

                            if is_relative_improvement:
                                exam_context.record_improvement()
                                relative_best = [exam_neighbor, penalty]

                                is_absolute_improvement \
                                    = penalty < absolute_best[1]

                                if is_absolute_improvement:
                                    block_context.record_improvement()
                                    absolute_best = [exam_neighbor, penalty]
                                    logger.log(f"New relative best: {penalty} ***")
                                else:
                                    logger.log(f"New relative best: {penalty}")

                            break

        logger.brag(absolute_best[1], start_time)
        return tuple(absolute_best)

    def _get_scored_exam_neighbors_of(self, current_solution: Schedule):
        """Return a list of [exam_neighbor, penalty] lists, sorted
        by the penalty.
        """
        return sorted(
            [
                [neighbor, self.evaluator.penalty(neighbor)]
                for neighbor in ExamNeighborhood(current_solution)
            ],
            key=lambda x: x[1]
        )

    def _get_initial_solution(self) -> Schedule:
        """Construct an initial solution that is the base for the search."""
        schedule, _ = RandomAssignment(self.data).run()
        return schedule
