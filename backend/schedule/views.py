from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ModelViewSet

from .models import AssessmentPhase
from .serializers import (
    AssessmentPhaseDetailSerializer,
    AssessmentPhaseListSerializer
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
