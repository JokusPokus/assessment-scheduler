"""
Conversion of in-memory schedule to useful output formats
"""
from exam.models import Exam
from schedule.models import (
    Window,
    Block,
    BlockSlot,
    BlockTemplate,
    ExamSlot,
    Schedule as DBSchedule,
)

from .schedule import Schedule, BlockSchedule, ExamSchedule


class DBOutputWriter:
    """Writes a Schedule instance to a normalized database representation."""
    def __init__(self, window: Window, schedule: Schedule, penalty: int):
        self.window = window
        self.schedule = schedule
        self.penalty = penalty

    def write_to_db(self) -> None:
        db_schedule = DBSchedule.objects.create(
            window=self.window,
            penalty=self.penalty
        )

        for slot_id, block_schedules in self.schedule.items():
            slot = BlockSlot.objects.get(id=slot_id)

            for block_schedule in block_schedules:
                block = Block.objects.create(
                    schedule=db_schedule,
                    block_slot=slot,
                    template=self._get_template_from(block_schedule)
                )
                for exam_schedule in block_schedule.exams:
                    self._create_and_link_exam_slot(
                        block,
                        block_schedule,
                        exam_schedule,
                    )

    def _get_template_from(self, block_schedule) -> BlockTemplate:
        return self.window.block_templates.get(
            exam_length=block_schedule.exam_length
        )

    def _create_and_link_exam_slot(
            self,
            block: Block,
            block_schedule: BlockSchedule,
            exam_schedule: ExamSchedule,
    ) -> None:
        exam_slot = ExamSlot.objects.create(
            block=block,
            start_time=exam_schedule.time_frame.start_time
        )
        exam = Exam.objects.get(
            code=exam_schedule.exam_code,
            window=self.window
        )
        exam.time_slot = exam_slot
        exam.helper = block_schedule.helper
        exam.save()


class CSVOutputWriter:
    """Takes a normalized database schedule and writes it to a CSV file."""

    def __init__(self, schedule: DBSchedule):
        self.schedule = schedule

    def write_to_csv(self):
        input_csv = self.schedule.window
        pass