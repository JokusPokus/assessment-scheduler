from rest_framework import serializers

from .models import Module


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = [
            'id',
            'code',
            'name',
            'standard_length',
            'alternative_length'
        ]
