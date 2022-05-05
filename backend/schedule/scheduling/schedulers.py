"""
Management and orchestration of the scheduling process
"""
from typing import Optional, Type
from pprint import pprint

from schedule.models import Window
from .algorithms import BaseAlgorithm, TabuSearch
from .evaluators import Evaluator
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
        algorithm = self.algorithm_class(data, self.evaluator)
        schedule = algorithm.run()
        pprint(schedule)
