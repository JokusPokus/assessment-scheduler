from rest_framework import serializers

from .models import (
    AssessmentPhase,
    Window,
)


class AssessmentPhaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentPhase
        fields = ['year', 'semester', 'category']


class AssessmentPhaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentPhase
        fields = ['year', 'semester', 'category', 'room_limit']
