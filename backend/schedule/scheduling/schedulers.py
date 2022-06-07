"""
Management and orchestration of the scheduling process
"""
from typing import Optional, Type
from pprint import pprint

from schedule.models import Window
from .algorithms import BaseAlgorithm, TabuSearch, UnfeasibleInputError
from .evaluators import Evaluator, ValidationError
from .input_collectors import BaseInputCollector, DBInputCollector
from .helpers import HelperAssigner
from .output_writers import DBOutputWriter, CSVOutputWriter


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
            helper_assigner: Optional[HelperAssigner] = None,
    ):
        self.window = window
        self.input_collector = input_collector or DBInputCollector(window)
        self.algorithm_class = algorithm_class or TabuSearch
        self.evaluator = evaluator or Evaluator()
        self.helper_assigner = helper_assigner or HelperAssigner()

    def run(self) -> None:
        """Execute all the steps given above."""
        data = self.input_collector.collect()
        self.evaluator.validate_availabilities(data)

        algorithm = self.algorithm_class(data, self.evaluator)
        schedule, penalty = algorithm.run()

        schedule = self.helper_assigner.assign_helpers(schedule, data)

        db_writer = DBOutputWriter(self.window, schedule, penalty)
        db_schedule = db_writer.write_to_db()

        print("Schedule was written to database!")

        CSVOutputWriter(db_schedule).write_to_csv()

        print("CSV saved in window instance")
