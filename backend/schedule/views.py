from django.db import transaction

from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.viewsets import ModelViewSet

from .models import AssessmentPhase, Window, BlockSlot
from .serializers import (
    AssessmentPhaseDetailSerializer,
    AssessmentPhaseListSerializer,
    WindowSerializer,
    BlockSlotSerializer
)
from .utils.datetime import combine
from staff.models import Assessor


class AssessmentPhaseViewSet(ModelViewSet):
    def get_serializer_class(self):
        """Select the serializer class based on the HTTP action."""
        if self.action == 'list':
            return AssessmentPhaseListSerializer
        if self.action == 'retrieve':
            return AssessmentPhaseDetailSerializer
        if self.action == 'create':
            return AssessmentPhaseListSerializer

        raise NotImplementedError

    def get_queryset(self):
        """Return all assessment phases that belong to the requesting
        user's organization.
        """
        return AssessmentPhase.objects.filter(
            organization=self.request.user.organization
        )

    @action(
        methods=['get'],
        detail=False,
        url_path='(?P<year>[A-Za-z0-9]*)/(?P<semester>[A-Za-z0-9]*)',
        url_name='get-by-attributes'
    )
    def get_by_attributes(self, request, year=None, semester=None):
        """Return serialized information about an assessment phase.

        The assessment phase can be specified via its year and semester
        attributes, respectively.
        """
        try:
            year = int(year)
        except ValueError:
            return Response(status=HTTP_400_BAD_REQUEST)

        try:
            phase = self.get_queryset().get(year=year, semester=semester)
        except AssessmentPhase.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        serializer = AssessmentPhaseDetailSerializer(phase)
        return Response(serializer.data, status=HTTP_200_OK)


class WindowViewSet(ModelViewSet):
    serializer_class = WindowSerializer

    def get_queryset(self):
        return Window.objects.filter(
            assessment_phase__organization=self.request.user.organization
        )

    @action(
        methods=['post'],
        detail=True,
        url_name='add-block-slots',
        url_path='add-block-slots'
    )
    @transaction.atomic
    def add_block_slots(self, request, pk=None):
        """Add block slots to a window.

        Prior block slots configuration is ignored in favor of the new data
        to be saved.
        """
        window = self.get_object()
        window.block_slots.all().delete()

        for date, start_times in request.data.items():
            for time in start_times:
                data = {
                    'date': date,
                    'time': time,
                    'window': window
                }
                serializer = BlockSlotSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        return Response(status=HTTP_200_OK)

    @action(
        methods=['post'],
        detail=True,
        url_name='add-assessor-availabilities',
        url_path='add-assessor-availabilities'
    )
    @transaction.atomic
    def add_assessor_availabilities(self, request, pk=None):
        """Add a new set of block slots to assessors' availabilities.

        The request body is expected to contain a key-value pair for each
        relevant assessor, where the key is the assessor's email and the value
        is a dictionary with dates as keys and the according block slot
        starting times as values.

        Consider the following example:

        request.data = {
            'assessor_1@code.berlin': {
                '2022-03-31': ['10:00', '14:00'],
                '2022-04-01': ['10:00']
            },
            'assessor_2@code.berlin': {
                '2022-04-01': ['14:00'],
                '2022-04-03': ['10:00', '14:00']
            }
        }
        """
        window = self.get_object()

        for assessor, availabilities in request.data.items():
            self._add_availabilities_for(assessor, availabilities, window)

        return Response(status=HTTP_200_OK)

    def _add_availabilities_for(self, assessor, availabilities, window):
        assessor = Assessor.objects.get(assessor)
        assessor.available_blocks.filter(window=window).delete()
        for date, times in availabilities.items():
            for time in times:
                self._add_available_slot(assessor, date, time, window)

    @staticmethod
    def _add_available_slot(assessor, date, time, window):
        start_time = combine(date, time)
        slot = BlockSlot.objects.get(
            window=window,
            start_time=start_time
        )
        assessor.available_blocks.add(slot)
