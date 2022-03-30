from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .serializers import PlanningSheetSerializer


class PlanningSheetView(CreateAPIView):
    """View to receive the general CSV planning sheet and initiates its
    processing.

    * Requires token authentication
    * Only Examination Office administrators can access this view
    """
    serializer_class = PlanningSheetSerializer
