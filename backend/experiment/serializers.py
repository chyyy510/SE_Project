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


class ExperimentCreateSerializer(serializers.Serializer):
    class Meta:
        model = Experiment
        fields = [
            "title",
            "description",
            # 默认已创建就是open
            "person_wanted",
            "money_per_person",
            # 先假定不付钱
        ]
