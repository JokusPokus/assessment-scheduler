"""
Management and orchestration of the scheduling process
"""
from typing import Optional

from schedule.models import Window
from .input_collectors import BaseInputCollector, DBInputCollector


class Scheduler:
    """Manages the scheduling process.

    In particular, the following steps are orchestrated:
        1. Input collection
        2. Algorithm execution
        3. Solution evaluation
        4. Saving of the solution
    """
    def __init__(
            self,
            window: Window,
            input_collector: Optional[BaseInputCollector] = None,
            algorithm=None,
            evaluator=None,
            output_writer=None
    ):
        self.window = window
        self.input_collector = input_collector or DBInputCollector(window)
        self.algorithm = algorithm
        self.evaluator = evaluator
        self.output_writer = output_writer

    def run(self):
        data = self.input_collector.collect()
        print(vars(data))
