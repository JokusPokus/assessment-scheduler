from datetime import datetime, timedelta

from rest_framework import serializers

from .models import (
    AssessmentPhase,
    Window,
    BlockSlot,
    BlockTemplate
)
from .utils.datetime import combine


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
        data['start_time'] = combine(data.pop('date'), data.pop('time'))
        self._validate_time(data)

        return data

    @staticmethod
    def create(validated_data):
        obj, _ = BlockSlot.objects.get_or_create(**validated_data)
        return obj

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
            if timedelta(0) < abs(time - data.get('start_time')) < min_distance:
                raise serializers.ValidationError(
                    {'start_time': 'Overlapping block slots'}
                )


class WindowSerializer(serializers.ModelSerializer):
    block_slots = BlockSlotSerializer(many=True, required=False)

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

    @staticmethod
    def create(validated_data, *args, **kwargs):
        obj = Window.objects.create(**validated_data)

        standard_block_templates = [
            BlockTemplate.objects.get(
                block_length=180,
                exam_length=20,
                exam_start_times=[0, 20, 40, 80, 100, 140, 160],
            ),
            BlockTemplate.objects.get(
                block_length=180,
                exam_length=30,
                exam_start_times=[0, 30, 60, 120, 150],
            ),
        ]

        obj.block_templates.add(*standard_block_templates)
        return obj


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
