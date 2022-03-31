from rest_framework import serializer

from .models import (
    AssessmentPhase,
    Window,
)


class AssessmentPhaseListSerializer(serializer.ModelSerializer):
    class Meta:
        model = AssessmentPhase
        fields = ['year', 'semester', 'category']


class AssessmentPhaseDetailSerializer(serializer.ModelSerializer):
    class Meta:
        model = AssessmentPhase
        fields = ['year', 'semester', 'category', 'room_limit']
