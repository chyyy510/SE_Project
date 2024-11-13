from rest_framework import serializers

from experiment.models import Experiment


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = "__all__"


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
