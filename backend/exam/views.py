from django.db import transaction

from rest_framework.decorators import action
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

    @action(
        methods=['post'],
        detail=False,
        url_path='add-durations',
        url_name='add-durations'
    )
    @transaction.atomic
    def add_durations(self, request):
        """Add or update duration attributes on a set of modules."""
        modules = request.data
        for module_data in modules:
            try:
                module = Module.objects.get(id=module_data['id'])
            except Module.DoesNotExist:
                return Response(status=HTTP_404_NOT_FOUND)

            module.standard_length = module_data['standard_length']
            module.alternative_length = module_data['alternative_length']
            module.save()

        return Response(status=HTTP_200_OK)
