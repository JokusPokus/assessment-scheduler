from rest_framework import serializers

from .models import PlanningSheet


class PlanningSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanningSheet
        fields = ['assessment_phase', 'csv']
