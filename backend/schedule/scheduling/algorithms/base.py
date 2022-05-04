"""
Abstract base class for algorithm implementations.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import reduce
from typing import Optional

from ..input_collectors import InputData
from ..evaluators import Evaluator
from ..types import Schedule


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
        exams = self.data.exams.values('code', 'assessor', 'student', 'module')

        # Do n times (with n = num of blocks to be assigned):

        #     1. Pick the most difficult slot:
        #         - lowest number of available assessors
        #         - tie breaker: lowest number of available helpers

        #     2. Among the assessors available for that slot, pick the most
        #        difficult one:
        #         - lowest availability surplus := avails - workload

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
