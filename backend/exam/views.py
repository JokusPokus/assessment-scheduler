from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from .models import Module
from .serializers import ModuleSerializer
from schedule.models import Window


class ModuleViewSet(ModelViewSet):
    serializer_class = ModuleSerializer

    def get_queryset(self):
        """Return all modules that belong to the requesting
        user's organization and assessment phase.
        """
        window_id = self.request.query_params.get('window')
        try:
            window = Window.objects.get(id=window_id)
        except Window.DoesNotExist:
            return Response(HTTP_404_NOT_FOUND)

        return Module.objects.filter(
            organization=self.request.user.organization
        )

