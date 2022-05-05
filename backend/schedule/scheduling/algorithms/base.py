"""
Abstract base class for algorithm implementations.
"""
from abc import ABC, abstractmethod
import random
from typing import Optional, List, ItemsView, Tuple

from staff.models import Assessor
from schedule.models import BlockTemplate

from ..input_collectors import InputData
from ..evaluators import Evaluator
from ..schedule import Schedule, BlockSchedule, ExamSchedule
from ..types import AvailInfo, SlotId


class BaseAlgorithm(ABC):
    """Defines an interface for algorithm implementations."""

    def __init__(
            self,
            data: InputData,
            evaluator: Optional[Evaluator] = None
    ):
        self.data = data
        self.evaluator = evaluator

    @abstractmethod
    def run(self) -> Schedule:
        """Solve the exam scheduling problem as defined by self.data and
        return the solution as a Schedule instance.
        """
        pass


class RandomAssignment(BaseAlgorithm):
    """Utility class for pseudo-random algorithm initialization."""

    def run(self) -> Schedule:
        """Randomly assign assessor blocks to available slots, and
        then exams to the blocks.

        Return the resulting schedule, which is not guaranteed to be
        free of first-order conflicts.
        """
        schedule = {}
        exams = self.data.exams.values('code', 'assessor', 'student', 'module')
        avails = self.data.staff_avails.items()

        for _ in range(self._num_blocks_to_assign):
            slot, avail_info = self._most_difficult_slot(avails)
            assessor = self._most_difficult_assessor(avail_info['assessors'])
            template = self._get_random_template_for(assessor)

            for start_time in template.exam_start_times:
                # assign exam to block
                pass

        #     3. Randomly choose an exam length of that assessor and fill
        #        a block of that length and assessor with random exams to
        #        be executed by the assessor.

        #     4. Assign that block to the slot.

        #     5. Update assessor workload, staff availabilities, exam list
        #

    @property
    def _num_blocks_to_assign(self) -> int:
        """Return the total number of blocks that need to be scheduled,
        that is, the sum of individual assessors' blocks.
        """
        return sum(
            [
                sum(block_count.values())
                for block_count in self.data.assessor_workload.values()
            ]
        )

    def _most_difficult_slot(
            self,
            avails: ItemsView[SlotId, AvailInfo]
    ) -> Tuple[SlotId, AvailInfo]:
        """Return a tuple of (slot code, availability info) for the
        slot that is currently most difficult to schedule.

        The difficulty assessment is based on the slot difficulty score.
        """
        return min(avails, key=self._slot_ease_score)

    @staticmethod
    def _slot_ease_score(slot: tuple) -> tuple:
        """Return the ease score for a given slot in the shape
        of a (assessor count, helper count) tuple.

        A lexicographic ordering underlies this score, with higher
        values indicating a higher potential for conflict-less
        scheduling.
        """
        _, avails = slot
        return avails['assessor_count'], avails['helper_count']

    def _most_difficult_assessor(self, assessors: List[Assessor]) -> Assessor:
        """Return the assessor who is most difficult to schedule,
        as indicated by the assessor difficulty scores.
        """
        return min(assessors, key=self._assessor_ease_score)

    def _assessor_ease_score(self, assessor: Assessor) -> int:
        """Return the assessor's availability surplus.

        The availability surplus is defined as the number of the
        assessor's available slots minus the blocks she needs to
        be scheduled for.

        The higher the availability surplus, the easier it is
        - heuristically - to schedule the assessor.
        """
        available_slots = assessor.available_blocks.count()

        workload = self.data.assessor_workload[assessor.email]
        blocks_to_schedule = sum(workload.values())

        return available_slots - blocks_to_schedule

    def _get_random_template_for(self, assessor) -> BlockTemplate:
        """Randomly return one of the possible block templates that the
        schedule still needs to cover for the given assessor.
        """
        length_options = self.data.assessor_workload[assessor.email].keys()
        exam_length = random.choice(length_options)
        return self.data.block_templates.get(exam_length=exam_length)
