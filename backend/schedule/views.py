from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.viewsets import ModelViewSet

from .models import AssessmentPhase, Window
from .serializers import (
    AssessmentPhaseDetailSerializer,
    AssessmentPhaseListSerializer,
    WindowSerializer
)


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
    def add_block_slots(self, request, pk=None):
        print(request.data)
        return Response(status=HTTP_200_OK)
