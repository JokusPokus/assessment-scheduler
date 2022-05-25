"""
Conversion of in-memory schedule to useful output formats
"""
import pandas as pd

from django.core.files.base import ContentFile

from exam.models import Exam
from input.models import PlanningSheet
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

    def write_to_db(self) -> DBSchedule:
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

        return db_schedule

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
        input_planning_sheet = self.schedule.window.planning_sheets.get(
            is_filled_out=False
        )

        data = pd.read_csv(input_planning_sheet.csv.path, sep=',')
        data[['startTime', 'endTime', 'assistant']] \
            = data.apply(self._schedule_decisions, axis=1)

        content = data.to_csv(index=False)
        temp_file = ContentFile(content.encode('utf-8'))

        output_planning_sheet = PlanningSheet(
            window=self.schedule.window,
            is_filled_out=True
        )

        output_planning_sheet.csv.save(self._file_name(), temp_file)
        output_planning_sheet.save()

    def _file_name(self) -> str:
        """Return a descriptive name for the csv output file."""
        phase = self.schedule.window.assessment_phase
        window_pos = self.schedule.window.position
        return f'schedule_{phase.semester}_{phase.year}' \
               f'_window_{window_pos}.csv'

    def _schedule_decisions(self, row) -> pd.Series:
        exam = Exam.objects.get(
            window=self.schedule.window,
            code=row['assessmentId']
        )

        start_time = exam.time_slot.start_time.strftime('%Y-%m-%d %H:%M')
        end_time = exam.time_slot.end_time.strftime('%Y-%m-%d %H:%M')
        helper = exam.helper.email if exam.helper else 'n.d.'

        return pd.Series([start_time, end_time, helper])
