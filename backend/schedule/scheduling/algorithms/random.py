"""
Utility classes for pseudo-random initialization.
"""
from collections import Counter
from datetime import timedelta
import random
from typing import List, Tuple

from django.db.models import Q, QuerySet

from staff.models import Assessor
from schedule.models import BlockTemplate
from exam.models import Exam, Module

from .back_tracking import BackTracking
from .base import BaseAlgorithm
from ..schedule import Schedule, BlockSchedule, ExamSchedule, TimeFrame


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
                template = self._get_random_template_for(block.assessor)

                block.start_time = self.data.block_slots.get(id=slot).start_time
                block.exam_start_times = template.exam_start_times
                block.exam_length = template.exam_length

                exam_candidates = self._get_compatible_exams(
                    block.assessor,
                    template
                )
                self._assign_compatible_exams(
                    block,
                    exam_candidates,
                    template
                )

                self.data.assessor_workload.decrement(
                    block.assessor,
                    template.exam_length
                )

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

        exam_length = random.choice(length_options)
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

    def _assign_compatible_exams(
            self,
            block: BlockSchedule,
            exam_candidates: QuerySet,
            template: BlockTemplate
    ) -> None:
        """From the queryset of exam candidates, pseudo-randomly assign
        exams to to the block and delete scheduled exams from the total list of
        exams.

        Since assessors shall jump between exam topics as little as
        possible, group the exam candidates by module and stick with one
        module as long as possible. Within the module group, exams are
        assigned randomly.

        If there are less candidates than exam slots in the template,
        just stop assigning.
        """
        def module_group_order(_exam: Exam) -> Tuple:
            """Return a tuple for lexicographic ordering of exams.

            The random number implements a shuffle within module groups.
            """
            ranking = ranked_modules.index(_exam.module)
            return ranking, random.random()

        candidates = list(exam_candidates)
        ranked_modules = self._get_modules_quantity_ranking(exam_candidates)

        candidates.sort(key=module_group_order)

        for i, rel_start_time in enumerate(template.exam_start_times):
            exam = self._add_exam(block, candidates, i, rel_start_time)

            self._update_exams(exam)

            if not candidates:
                break

    @staticmethod
    def _add_exam(
            block: BlockSchedule,
            candidates: List[Exam],
            position: int,
            rel_start_time: int
    ) -> Exam:
        """Take the first exam from the candidates list and append it to
        the block's exam list.
        """
        exam = candidates.pop(0)
        abs_start_time = block.start_time + timedelta(minutes=rel_start_time)
        abs_end_time = abs_start_time + timedelta(minutes=block.exam_length)
        block.exams.append(
            ExamSchedule(
                exam_code=exam.code,
                module=exam.module,
                student=exam.student,
                position=position,
                time_frame=TimeFrame(abs_start_time, abs_end_time)
            )
        )
        return exam

    @staticmethod
    def _get_modules_quantity_ranking(
            exam_candidates: List[Exam]
    ) -> List[Module]:
        """Return a list of modules ranked by the number of occurrences
        in the exam list, from high to low.
        """
        counter = Counter([exam.module for exam in exam_candidates])
        return [module for module, count in counter.most_common()]

    @staticmethod
    def _fitting_length_query(length: int):
        """Complex Django query to filter for exams that have
        the given length.
        """
        return (
                (Q(style='alternative') & Q(module__alternative_length=length))
                | (Q(style='standard') & Q(module__standard_length=length))
        )

    def _update_exams(self, exam: Exam) -> None:
        """Remove the exam from the queryset of exams s.t. it is no longer
        considered in the scheduling process.
        """
        self.data.exams = self.data.exams.exclude(id=exam.id)
