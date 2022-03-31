from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ModelViewSet

from .models import AssessmentPhase
from .serializers import (
    AssessmentPhaseDetailSerializer,
    AssessmentPhaseListSerializer
)


class AssessmentPhaseViewSet(ModelViewSet):
    def get_queryset(self):
        """Return all assessment phases that belong to the requesting user's
        organization.
        """
        return AssessmentPhase.objects.filter(
            organization=self.request.user.organization
        )
