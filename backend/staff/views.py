from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from .models import Assessor
from .serializers import AssessorSerializer
from schedule.models import Window


class AssessorViewSet(ReadOnlyModelViewSet):
    serializer_class = AssessorSerializer

    def get_queryset(self):
        """Return all assessment phases that belong to the requesting
        user's organization.
        """
        window_id = self.request.query_params.get('window')
        try:
            window = Window.objects.get(id=window_id)
        except Window.DoesNotExist:
            return Response(HTTP_404_NOT_FOUND)

        return Assessor.objects.filter(
            organization=self.request.user.organization,
            assessment_phases=window.assessment_phase
        )
