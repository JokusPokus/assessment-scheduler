from rest_framework import serializers

from .models import (
    AssessmentPhase,
    Window,
)


class WindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Window
        fields = ['id', 'start_date', 'end_date']


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
        fields = ['year', 'semester', 'category', 'room_limit', 'windows']
        depth = 1
