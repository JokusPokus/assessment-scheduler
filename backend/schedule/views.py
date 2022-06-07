from typing import Type, Union

from django.db import transaction
from django.http import HttpResponse

from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.viewsets import ModelViewSet

from .models import AssessmentPhase, Window, BlockSlot, Schedule
from .scheduling import Scheduler
from .serializers import (
    AssessmentPhaseDetailSerializer,
    AssessmentPhaseListSerializer,
    WindowSerializer,
    BlockSlotSerializer
)
from .utils.datetime import combine
from input.models import PlanningSheet
from staff.models import Assessor, Helper, Staff


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

        window_ids = []
        for date, start_times in request.data.items():
            for time in start_times:
                slot = self._get_or_create_slot(date, time, window)
                window_ids.append(slot.id)

        self._delete_obsolete_slots(window, window_ids)

        return Response(status=HTTP_200_OK)

    @action(
        methods=['delete'],
        detail=True,
        url_name='remove-staff',
        url_path='remove-staff'
    )
    def remove_staff(self, request, pk=None):
        """Remove a staff member from the current window's planning.

        The staff member is identified by their email address as given
        in the request body.
        """
        window = self.get_object()
        try:
            helper = Helper.objects.get(email=request.data.get('email'))
        except Helper.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        helper.assessment_phases.remove(window.assessment_phase)
        helper.available_blocks.remove(
            *helper.available_blocks.filter(window=window)
        )

        return Response(status=HTTP_200_OK)

    @action(
        methods=['post'],
        detail=True,
        url_name='add-staff-availabilities',
        url_path='add-staff-availabilities'
    )
    @transaction.atomic
    def add_staff_availabilities(self, request, pk=None):
        """Add a new set of block slots to staff availabilities.

        The request body is expected to contain a key-value pair for each
        relevant assessor, where the key is the staff member's email and the
        value is a dictionary with dates as keys and the according block slot
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

        staff_class = {
            'assessors': Assessor,
            'helpers': Helper
        }[request.query_params.get('resource')]

        for email, availabilities in request.data.items():
            if staff_class == Helper:
                self._create_or_update_helper(email, request, window)

            self._add_availabilities_for(
                email,
                staff_class,
                availabilities,
                window
            )

        return Response(status=HTTP_200_OK)

    @action(
        methods=['get'],
        detail=True,
        url_name='trigger-scheduling',
        url_path='trigger-scheduling'
    )
    def trigger_scheduling(self, request, pk=None):
        """Trigger the scheduling process."""
        window = self.get_object()
        window.scheduling_ongoing = True
        window.save()

        try:
            Scheduler(window).run()
        except Exception as e:
            window.scheduling_ongoing = False
            window.save()
            raise e

        window.scheduling_ongoing = False
        window.save()

        return Response(HTTP_200_OK)

    @action(
        methods=['get'],
        detail=True,
        url_name='scheduling-status',
        url_path='scheduling-status'
    )
    def scheduling_status(self, request, pk=None):
        """Determine a window's scheduling status."""
        window = self.get_object()

        if window.scheduling_ongoing:
            scheduling_status = 'ongoing'
        elif window.planning_sheets.filter(is_filled_out=True).exists():
            scheduling_status = 'done'
        else:
            scheduling_status = 'idle'

        return Response(
            {'scheduling_status': scheduling_status},
            status=HTTP_200_OK
        )

    @action(
        methods=['get'],
        detail=True,
        url_name='schedule-evaluation',
        url_path='schedule-evaluation'
    )
    def schedule_evaluation(self, request, pk=None):
        """Get the window's latest schedule's evaluation stats."""
        window = self.get_object()

        try:
            schedule = window.schedules.latest('created')
        except Schedule.DoesNotExist:
            penalty = None
        else:
            penalty = schedule.penalty

        return Response(
            {'penalty': penalty},
            status=HTTP_200_OK
        )

    @action(
        methods=['get'],
        detail=True,
        url_name='get-csv',
        url_path='get-csv'
    )
    def get_csv(self, request, pk=None):
        """Get the window's latest csv planning sheet."""
        window = self.get_object()

        try:
            planning_sheet = window.planning_sheets\
                .filter(is_filled_out=True)\
                .latest('created')
        except PlanningSheet.DoesNotExist:
            return Response(HTTP_404_NOT_FOUND)

        response = HttpResponse(
            planning_sheet.csv,
            content_type='text/csv',
            status=HTTP_200_OK
        )
        response['Content-Disposition'] = f'attachment; filename={planning_sheet.csv.name}'
        return response

    @staticmethod
    def _delete_obsolete_slots(window, window_ids):
        window.block_slots.exclude(id__in=window_ids).delete()

    @staticmethod
    def _get_or_create_slot(date, time, window):
        data = {
            'date': date,
            'time': time,
            'window': window
        }
        serializer = BlockSlotSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        slot = serializer.save()
        return slot

    @staticmethod
    def _create_or_update_helper(email, request, window):
        helper, _ = Helper.objects.get_or_create(
            organization=request.user.organization,
            email=email
        )
        helper.windows.add(window)

    def _add_availabilities_for(
            self,
            email: str,
            staff_class: Type[Staff],
            availabilities: dict,
            window: Window
    ) -> None:
        staff = staff_class.objects.get(email=email)
        staff.available_blocks.remove(
            *staff.available_blocks.filter(window=window)
        )
        for date, times in availabilities.items():
            for time in times:
                self._add_available_slot(staff, date, time, window)

    @staticmethod
    def _add_available_slot(
            staff: Staff,
            date: str,
            time: str,
            window: Window
    ) -> None:
        start_time = combine(date, time)
        slot = BlockSlot.objects.get(
            window=window,
            start_time=start_time
        )
        staff.available_blocks.add(slot)
