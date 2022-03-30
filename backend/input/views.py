from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import PlanningSheetSerializer


class PlanningSheetView(CreateModelMixin, GenericViewSet):
    """View to receive the general CSV planning sheet and initiates its
    processing.

    * Requires token authentication
    * Only Examination Office administrators can access this view
    """
    serializer_class = PlanningSheetSerializer
