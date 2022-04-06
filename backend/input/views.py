import io
import pandas as pd

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.parsers import MultiPartParser

from .serializers import PlanningSheetSerializer
from schedule.models import Window


class PlanningSheetUploadView(generics.CreateAPIView):
    parser_classes = [MultiPartParser]

    def post(self, request, filename, format=None):
        """View to receive the general CSV planning sheet and initiates its
        processing.

        * Requires token authentication
        * Only Examination Office administrators can access this view
        """
        window_id = request.data.get('window')
        if not window_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not Window.objects.filter(
                id=window_id,
                assessment_phase__organization=request.user.organization
        ).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = PlanningSheetSerializer(
            data={
                'csv': request.data.get('planningSheet'),
                'window': window_id
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
