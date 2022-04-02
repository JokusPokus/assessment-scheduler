from rest_framework import serializers

from .models import (
    AssessmentPhase,
    Window,
)


class WindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Window
        fields = [
            'id',
            'position',
            'assessment_phase',
            'start_date',
            'end_date',
            'block_length'
        ]


class AssessmentPhaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentPhase
        fields = [
            'id',
            'year',
            'semester',
            'category',
        ]


class AssessmentPhaseDetailSerializer(serializers.ModelSerializer):
    windows = WindowSerializer(many=True)

    class Meta:
        model = AssessmentPhase
        fields = [
            'id',
            'year',
            'semester',
            'category',
            'room_limit',
            'windows'
        ]
        depth = 1
