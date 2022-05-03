from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from .models import Assessor, Helper
from .serializers import AssessorSerializer, HelperSerializer
from schedule.models import Window


class AssessorViewSet(ReadOnlyModelViewSet):
    serializer_class = AssessorSerializer

    def get_queryset(self):
        """Return all assessors that belong to the requesting
        user's organization and assessment phase.
        """
        window_id = self.request.query_params.get('window')
        try:
            window = Window.objects.get(id=window_id)
        except Window.DoesNotExist:
            return Response(HTTP_404_NOT_FOUND)

        return Assessor.objects.filter(
            organization=self.request.user.organization,
            windows=window
        )


class HelperViewSet(ReadOnlyModelViewSet):
    serializer_class = HelperSerializer

    def get_queryset(self):
        """Return all helpers that belong to the requesting
        user's organization and assessment phase.
        """
        window_id = self.request.query_params.get('window')
        try:
            window = Window.objects.get(id=window_id)
        except Window.DoesNotExist:
            return Response(HTTP_404_NOT_FOUND)

        return Helper.objects.filter(
            organization=self.request.user.organization,
            windows=window
        )
