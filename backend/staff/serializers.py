from rest_framework import serializers

from .models import Assessor


class AssessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessor
        fields = ['email']
