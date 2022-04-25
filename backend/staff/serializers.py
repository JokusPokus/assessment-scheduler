from rest_framework import serializers

from .models import Assessor
from schedule.serializers import BlockSlotSerializer


class AssessorSerializer(serializers.ModelSerializer):
    available_blocks = BlockSlotSerializer(read_only=True, many=True)

    class Meta:
        model = Assessor
        fields = ['email', 'available_blocks']
        depth = 1
