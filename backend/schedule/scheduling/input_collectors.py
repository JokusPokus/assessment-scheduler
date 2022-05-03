"""
Input collection to working memory for scheduling purposes
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.db.models import QuerySet


class BaseInputCollector(ABC):
    """Defines an interface for input collector classes."""

    @abstractmethod
    def collect(self) -> InputData:
        pass


@dataclass
class InputData:
    """Defines the input data requirements for
    any scheduling algorithm.
    """

    exams: QuerySet
    modules: QuerySet
    assessors: QuerySet
    helpers: QuerySet
    students: QuerySet
    block_slots: QuerySet
    block_templates: QuerySet
