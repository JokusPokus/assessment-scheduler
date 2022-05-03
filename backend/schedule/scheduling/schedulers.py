"""
Management and orchestration of the scheduling process
"""
from schedule.models import Window


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
            input_collector,
            algorithm,
            evaluator,
            output_writer
    ):
        self.window = window
        self.input_collector = input_collector
        self.algorithm = algorithm
        self.evaluator = evaluator
        self.output_writer = output_writer

    def run(self):
        raise NotImplementedError
