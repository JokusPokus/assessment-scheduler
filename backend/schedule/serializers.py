from datetime import datetime

from django.utils.timezone import make_aware
from rest_framework import serializers

from .models import (
    AssessmentPhase,
    Window,
    BlockSlot
)


class BlockSlotSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField('get_date_portion', read_only=True)
    time = serializers.SerializerMethodField('get_time_portion', read_only=True)

    class Meta:
        model = BlockSlot
        fields = [
            'id',
            'date',
            'time',
            'window',
            'start_time'
        ]
        extra_kwargs = {
            'start_time': {'write_only': True}
        }

    @staticmethod
    def get_date_portion(obj):
        return obj.start_time.day

    @staticmethod
    def get_time_portion(obj):
        return obj.start_time.strftime("HH-MM")

    @staticmethod
    def to_internal_value(data):
        """Combine the date and time of a block slot to a proper datetime
        object.
        """
        date = datetime.strptime(data.pop('date'), '%Y-%m-%d')
        time = datetime.strptime(data.pop('time'), '%H:%M').time()

        start_time = datetime.combine(date, time)

        return {**data, 'start_time': make_aware(start_time)}


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
