from copy import deepcopy
from typing import Tuple, Dict, List

from staff.models import Assessor

from .base import BaseAlgorithm, UnfeasibleInputError
from ..input_collectors import AvailInfo, AssessorWorkload
from ..schedule import Schedule, BlockSchedule
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
                if assessor in info.assessors and info.helper_count
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
