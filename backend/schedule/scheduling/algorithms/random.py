"""
Utility classes for pseudo-random initialization.
"""
from copy import deepcopy
from datetime import datetime, timedelta
import random
from typing import Optional, List, ItemsView, Tuple, Dict

from django.db.models import Q, QuerySet

from staff.models import Assessor
from schedule.models import BlockTemplate

from .base import BaseAlgorithm
from ..input_collectors import InputData
from ..evaluators import Evaluator
from ..schedule import Schedule, BlockSchedule, ExamSchedule, TimeFrame
from ..types import AvailInfo, SlotId


class RandomAssignment(BaseAlgorithm):
    """Utility class for pseudo-random algorithm initialization."""

    def __init__(self, data):
        super().__init__(deepcopy(data))

    def run(self) -> Schedule:
        """Randomly assign assessor blocks to available slots, and
        then exams to the blocks.

        Return the resulting schedule, which is not guaranteed to be
        free of first-order conflicts.
        """
        schedule = Schedule()

        for _ in range(self.data.total_num_blocks):
            slot, avail_info = self._most_difficult_slot(self.data.staff_avails)
            assessor = self._most_difficult_assessor(avail_info['assessors'])
            template = self._get_random_template_for(assessor)

            block = BlockSchedule(
                start_time=self.data.block_slots.get(id=slot).start_time,
                exam_start_times=template.exam_start_times,
                assessor=assessor,
                exam_length=template.exam_length
            )

            exam_candidates = self._get_compatible_exams(assessor, template)
            self._randomly_assign_compatible_exams(block, exam_candidates, template)

            schedule[slot] += [block]

            self._update_availabilities(assessor, slot)
            self._update_workloads(assessor, template)

        return schedule

    def _most_difficult_slot(
            self,
            avails: Dict[SlotId, AvailInfo]
    ) -> Tuple[SlotId, AvailInfo]:
        """Return a tuple of (slot code, availability info) for the
        slot that is currently most difficult to schedule.

        The difficulty assessment is based on the slot difficulty score.
        """
        return min(avails.items(), key=self._slot_ease_score)

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
        available_slots = assessor.available_blocks.filter(
            window=self.data.window
        ).count()

        workload = self.data.assessor_workload[assessor.email]
        blocks_to_schedule = sum(workload.values())

        return available_slots - blocks_to_schedule

    def _get_random_template_for(self, assessor: Assessor) -> BlockTemplate:
        """Randomly return one of the possible block templates that the
        schedule still needs to cover for the given assessor.
        """
        length_options = self.data.assessor_workload[assessor.email].keys()
        exam_length = random.choice(list(length_options))
        return self.data.block_templates.get(exam_length=exam_length)

    def _get_compatible_exams(
            self,
            assessor: Assessor,
            template: BlockTemplate
    ) -> Queryset:
        """Return a queryset of exams that are executed by the assessor
        and conform with the template's exam length.
        """
        return self.data.exams \
            .filter(assessor=assessor) \
            .filter(self._fitting_length_query(template.exam_length))

    def _randomly_assign_compatible_exams(
            self,
            block: BlockSchedule,
            exam_candidates: QuerySet,
            template: BlockTemplate
    ) -> None:
        """From the queryset of exam candidates, randomly assign exams to
        to the block.

        If there are less candidates than exam slots in the template,
        just stop assigning.
        """
        for i, rel_start_time in enumerate(template.exam_start_times):
            exam = random.choice(exam_candidates)
            abs_start_time = block.start_time + timedelta(minutes=rel_start_time)
            abs_end_time = abs_start_time + timedelta(minutes=block.exam_length)
            block.exams.append(
                ExamSchedule(
                    exam_code=exam.code,
                    student=exam.student,
                    position=i,
                    time_frame=TimeFrame(abs_start_time, abs_end_time)
                )
            )
            exam_candidates = exam_candidates.exclude(id=exam.id)
            self.data.exams = self.data.exams.exclude(id=exam.id)

            if not exam_candidates:
                break

    @staticmethod
    def _fitting_length_query(length: int):
        """Complex Django query to filter for exams that have
        the given length.
        """
        return (
                (Q(style='alternative') & Q(module__alternative_length=length))
                | (Q(style='standard') & Q(module__standard_length=length))
        )

    def _update_workloads(
            self,
            assessor: Assessor,
            template: BlockTemplate
    ) -> None:
        """Reduce the assessor's workload by one.

        If this leads to empty workloads, delete them altogether.
        """
        if self.data.assessor_workload[assessor.email][template.exam_length] > 1:
            self.data.assessor_workload[assessor.email][template.exam_length] -= 1
        else:
            if len(self.data.assessor_workload[assessor.email]) == 1:
                del self.data.assessor_workload[assessor.email]

                for slot, avail_info in deepcopy(self.data.staff_avails).items():
                    if assessor in avail_info['assessors']:
                        if avail_info['assessor_count'] > 1:
                            self.data.staff_avails[slot]['assessors'].remove(assessor)
                            self.data.staff_avails[slot]['assessor_count'] -= 1
                        else:
                            del self.data.staff_avails[slot]

            else:
                del self.data.assessor_workload[assessor.email][template.exam_length]

    def _update_availabilities(
            self,
            assessor: Assessor,
            slot: SlotId
    ) -> None:
        """Reduce the assessor's availabilities by one.

        If this leads to empty availabilities, delete them altogether.
        """
        if self.data.staff_avails[slot]['assessor_count'] > 1:
            self.data.staff_avails[slot]['assessors'].remove(assessor)
            self.data.staff_avails[slot]['assessor_count'] -= 1
        else:
            del self.data.staff_avails[slot]
