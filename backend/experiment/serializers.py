from rest_framework import serializers

from .models import Experiment


class ExperimentSerializer(serializers.Serializer):
    class Meta:
        model = Experiment
        fields = [
            "id",
            "title",
            "status",
            "creator",
            "person_wanted",
            "person_already",
        ]
