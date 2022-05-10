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

from .base import BaseAlgorithm, UnfeasibleInputError
from ..input_collectors import InputData, AvailInfo, AssessorWorkload
from ..evaluators import Evaluator
from ..schedule import Schedule, BlockSchedule, ExamSchedule, TimeFrame
from ..types import SlotId


class SchedulingHeuristics:
    """Provides heuristic scores of scheduling difficulty to rank
    elements of the scheduling process.
    """

    @staticmethod
    def slot_ease_score(slot: Tuple[SlotId, AvailInfo]) -> Tuple[int, int]:
        """Return the ease score for a given slot in the shape
        of a (assessor count, helper count) tuple.

        A lexicographic ordering underlies this score, with higher
        values indicating a higher potential for conflict-less
        scheduling.
        """
        _, avails = slot
        return avails.assessor_count, avails.helper_count

    @staticmethod
    def assessor_ease_score(
            assessor: Assessor,
            staff_avails: Dict[SlotId, AvailInfo],
            assessor_workload: AssessorWorkload
    ) -> int:
        """Return the assessor's availability surplus.

        The availability surplus is defined as the number of the
        assessor's available slots minus the blocks she needs to
        be scheduled for.

        The higher the availability surplus, the easier it is
        - heuristically - to schedule the assessor.
        """
        available_slots = sum(
            [
                1
                for info in staff_avails.values()
                if assessor in info.assessors
            ]
        )
        blocks_to_schedule = assessor_workload[assessor]['remaining_workload']

        return available_slots - blocks_to_schedule


class BackTracking(BaseAlgorithm):
    """A depth-first back-tracking search guided by heuristics to find
    a feasible assessor-slot assignment (ignoring concrete exams).
    """
    def __init__(self, data, heuristics=None):
        super().__init__(data)
        self.heuristics = heuristics or SchedulingHeuristics()

    def run(self) -> Schedule:
        assessor_workload = self.data.assessor_workload
        for assessor in assessor_workload:
            assessor_workload[assessor]['remaining_workload'] = \
                assessor_workload.remaining_blocks_of(assessor)

        return self.back_track(
            Schedule(),
            self.data.staff_avails,
            assessor_workload
        )

    def back_track(
            self,
            schedule: Schedule,
            staff_avails: Dict[SlotId, AvailInfo],
            assessor_workload: AssessorWorkload
    ):
        if schedule.total_blocks_scheduled == self.data.total_num_blocks:
            return schedule

        schedule = deepcopy(schedule)
        staff_avails = deepcopy(staff_avails)
        assessor_workload = deepcopy(assessor_workload)

        slots = self._get_ranked_slots(staff_avails)

        if not slots:
            # This path has lead to a dead end!
            return None

        for slot in slots:
            available_assessors = staff_avails[slot].assessors
            ranked_assessors = self._get_ranked_assessors(
                available_assessors,
                staff_avails,
                assessor_workload
            )
            for assessor in ranked_assessors:
                schedule[slot] += [BlockSchedule(assessor)]

                self._update_avails(
                    staff_avails,
                    slot,
                    assessor
                )
                self._update_workload(
                    assessor_workload,
                    staff_avails,
                    assessor
                )

                solution = self.back_track(
                    schedule,
                    staff_avails,
                    assessor_workload
                )

                if solution is None:
                    continue

                return solution

            raise UnfeasibleInputError

    def _get_ranked_slots(
            self,
            avails: Dict[SlotId, AvailInfo]
    ) -> List[SlotId]:
        """Return a list of slot ids, ranked according to the (heuristic)
        scheduling difficulty.

        This ranking depends on the current state of the scheduling
        process, i.e., the current assessor workloads and availabilities.
        """
        non_empty_avails = [
            (slot, info)
            for slot, info in avails.items()
            if info.assessor_count and info.helper_count
        ]
        non_empty_avails.sort(key=self.heuristics.slot_ease_score)
        return [slot for slot, info in non_empty_avails]

    def _get_ranked_assessors(
            self,
            assessors: List[Assessor],
            staff_avails: Dict[SlotId, AvailInfo],
            assessor_workload: AssessorWorkload
    ) -> List[Assessor]:
        """Return a list of assessors, ranked according to the (heuristic)
        scheduling difficulty.

        This ranking depends on the current state of the scheduling
        process, i.e., the current assessor workloads and availabilities.
        """
        def assessor_ease(assessor):
            return self.heuristics.assessor_ease_score(
                assessor,
                staff_avails,
                assessor_workload
            )
        return sorted(assessors, key=assessor_ease)

    def _update_workload(
            self,
            assessor_workload: AssessorWorkload,
            staff_avails: Dict[SlotId, AvailInfo],
            assessor: Assessor,
    ) -> None:
        """Reduce the assessor's workload by one.

        If no more blocks are pending for this assessor, remove her from
        the staff availabilities altogether.
        """
        assessor_workload[assessor]['remaining_workload'] -= 1

        if not assessor_workload[assessor]['remaining_workload']:
            self._remove_assessor_from_all_avails(staff_avails, assessor)

    @staticmethod
    def _remove_assessor_from_all_avails(
            staff_avails: Dict[SlotId, AvailInfo],
            assessor: Assessor
    ) -> None:
        """Remove the assessor from all the staff avail assessor lists."""
        for slot, avail_info in staff_avails.items():
            if assessor in avail_info.assessors:
                staff_avails[slot].remove(assessor)

    @staticmethod
    def _update_avails(
            staff_avails: Dict[SlotId, AvailInfo],
            slot: SlotId,
            assessor: Assessor
    ) -> None:
        """Remove assessor from the block's avails list and decrement both
        the assessor and helper counters.
        """
        staff_avails[slot].remove(assessor)
        staff_avails[slot].helper_count -= 1


class RandomAssignment(BaseAlgorithm):
    """Utility class for pseudo-random algorithm initialization."""

    def __init__(self, data, slot_assigner=None):
        super().__init__(data)
        self.slot_assigner = slot_assigner or BackTracking(data)

    def run(self) -> Schedule:
        """Using a back-tracking result for assessor-slot assignment,
        randomly assign concrete exams with conforming assessor and
        exam time.

        Return the resulting schedule, which is not guaranteed to be
        free of first-order conflicts.
        """
        schedule = self.slot_assigner.run()

        for slot, blocks in schedule.items():
            for block in blocks:
                print(f"Assessor {block.assessor.email} was assigned a block in slot {slot}")


            # slot, avail_info = self._most_difficult_slot(
            #     self.data.staff_avails
            # )
            # assessor = self._most_difficult_assessor(avail_info.assessors)
            # template = self._get_random_template_for(assessor)
            #
            # block = BlockSchedule(
            #     start_time=self.data.block_slots.get(id=slot).start_time,
            #     exam_start_times=template.exam_start_times,
            #     assessor=assessor,
            #     exam_length=template.exam_length
            # )
            #
            # exam_candidates = self._get_compatible_exams(assessor, template)
            # self._randomly_assign_compatible_exams(
            #     block,
            #     exam_candidates,
            #     template
            # )
            #
            # schedule[slot] += [block]
            #
            # self._update_availabilities(assessor, slot)
            # self._update_workloads(assessor, template)

        return schedule

    def _get_random_template_for(self, assessor: Assessor) -> BlockTemplate:
        """Randomly return one of the possible block templates that the
        schedule still needs to cover for the given assessor.
        """
        length_options = [
            length
            for length, count in self.data.assessor_workload[assessor].items()
            if count > 0
        ]
        exam_length = random.choice(list(length_options))
        return self.data.block_templates.get(exam_length=exam_length)

    def _get_compatible_exams(
            self,
            assessor: Assessor,
            template: BlockTemplate
    ) -> QuerySet:
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
        to the block and delete scheduled exams from the total list of
        exams.

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
