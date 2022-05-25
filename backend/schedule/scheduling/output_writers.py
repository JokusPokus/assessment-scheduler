"""
Conversion of in-memory schedule to useful output formats
"""
from exam.models import Exam
from schedule.models import BlockSlot, Block, ExamSlot, BlockTemplate

from .schedule import Schedule, BlockSchedule, ExamSchedule


class DBOutputWriter:
    """Writes a Schedule instance to a normalized database representation."""
    def __init__(self, schedule: Schedule):
        self.schedule = schedule

    def write_to_db(self) -> None:
        for slot_id, block_schedules in self.schedule.items():
            slot = BlockSlot.objects.get(id=slot_id)

            for block_schedule in block_schedules:
                block = Block.objects.create(
                    slot=slot,
                    template=self._get_template_from(block_schedule, slot)
                )
                for exam_schedule in block_schedule.exams:
                    self._create_and_link_exam_slot(
                        block,
                        block_schedule,
                        exam_schedule,
                        slot
                    )

    @staticmethod
    def _get_template_from(block_schedule, slot) -> BlockTemplate:
        return slot.window.block_templates.get(
            exam_length=block_schedule.exam_length
        )

    @staticmethod
    def _create_and_link_exam_slot(
            block: Block,
            block_schedule: BlockSchedule,
            exam_schedule: ExamSchedule,
            slot: BlockSlot
    ) -> None:
        exam_slot = ExamSlot.objects.create(
            block=block,
            start_time=exam_schedule.time_frame.start_time
        )
        exam = Exam.objects.get(
            code=exam_schedule.exam_code,
            window=slot.window
        )
        exam.time_slot = exam_slot
        exam.helper = block_schedule.helper
        exam.save()
