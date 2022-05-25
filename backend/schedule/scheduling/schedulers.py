"""
Management and orchestration of the scheduling process
"""
from typing import Optional, Type
from pprint import pprint

from schedule.models import Window
from .algorithms import BaseAlgorithm, TabuSearch, UnfeasibleInputError
from .evaluators import Evaluator, ValidationError
from .input_collectors import BaseInputCollector, DBInputCollector
from .output_writers import DBOutputWriter


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
            algorithm_class: Optional[Type[BaseAlgorithm]] = None,
            evaluator: Optional[Evaluator] = None,
            output_writer=None
    ):
        self.window = window
        self.input_collector = input_collector or DBInputCollector(window)
        self.algorithm_class = algorithm_class or TabuSearch
        self.evaluator = evaluator or Evaluator()
        self.output_writer = output_writer

    def run(self) -> None:
        """Execute all the steps given above."""
        data = self.input_collector.collect()
        try:
            self.evaluator.validate_availabilities(data)
        except ValidationError as e:
            print("Insufficient avails:", e.insufficient_avails)
            print("Helpers needed?", e.helpers_needed)
            raise e

        algorithm = self.algorithm_class(data, self.evaluator)
        try:
            schedule, penalty = algorithm.run(verbose=True)
        except UnfeasibleInputError as e:
            print("Input does not allow for valid schedule!")
            raise e

        DBOutputWriter(self.window, schedule, penalty).write_to_db()
        print("Schedule was written to database!")
