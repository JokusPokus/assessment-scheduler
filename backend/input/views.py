import io
import pandas as pd

from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from rest_framework.parsers import MultiPartParser

from schedule.models import Window


class PlanningSheetUploadView(views.APIView):
    parser_classes = [MultiPartParser]

    def put(self, request, filename, format=None):
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

        csv = request.data.get('planningSheet')
        data = pd.read_csv(csv.temporary_file_path())
        print(window_id)
        print(data)
        return Response(status=status.HTTP_200_OK)
