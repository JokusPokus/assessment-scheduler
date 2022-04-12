from rest_framework import serializers

from .models import PlanningSheet
from .validation import SheetValidator


class PlanningSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanningSheet
        fields = ['window', 'csv']

    @staticmethod
    def validate_csv(file):
        SheetValidator(file).validate()
        return file
