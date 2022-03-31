from rest_framework import serializers

from .models import (
    AssessmentPhase,
    Window,
)


class AssessmentPhaseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentPhase
        fields = [
            'year',
            'semester',
            'category',
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {
            **rep,
            'semester': instance.get_semester_display(),
            'category': instance.get_category_display()
        }


class AssessmentPhaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentPhase
        fields = ['year', 'semester', 'category', 'room_limit']
