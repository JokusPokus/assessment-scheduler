from datetime import datetime, timedelta

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
        return obj.start_time.strftime("%Y-%m-%d")

    @staticmethod
    def get_time_portion(obj):
        return obj.start_time.strftime("%H:%M")

    def to_internal_value(self, data):
        """Combine the date and time of a block slot to a proper datetime
        object.
        """
        date = datetime.strptime(data.pop('date'), '%Y-%m-%d')
        time = datetime.strptime(data.pop('time'), '%H:%M').time()

        start_time = datetime.combine(date, time)
        data['start_time'] = make_aware(start_time)

        self._validate_time(data)

        return data

    @staticmethod
    def _validate_time(data):
        """Validate that there is no other block slot interfering with
        the current one.

        If at least one other block slot too early or not early enough
        to avoid conflict, raise a ValidationError.
        """
        window = data.get('window')
        min_distance = timedelta(minutes=window.block_length)
        start_times = window.block_slots.all().values_list('start_time', flat=True)

        for time in start_times:
            if abs(time - data.get('start_time')) < min_distance:
                raise serializers.ValidationError(
                    {'start_time': 'Overlapping block slots'}
                )


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
