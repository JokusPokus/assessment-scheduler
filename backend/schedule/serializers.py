from rest_framework import serializers

from .models import (
    AssessmentPhase,
    Window,
    BlockSlot
)


class BlockSlotSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField('get_date_portion')
    time = serializers.SerializerMethodField('get_time_portion')

    class Meta:
        model = BlockSlot
        fields = [
            'id',
            'date',
            'time',
        ]

    @staticmethod
    def get_date_portion(obj):
        return obj.start_time.day

    @staticmethod
    def get_time_portion(obj):
        return obj.start_time.strftime("HH-MM")


class WindowSerializer(serializers.ModelSerializer):
    block_slots = BlockSlotSerializer(many=True)

    class Meta:
        model = Window
        fields = [
            'id',
            'position',
            'assessment_phase',
            'start_date',
            'end_date',
            'block_length',
            'block_slots',
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
        depth = 2
