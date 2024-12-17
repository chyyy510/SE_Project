from rest_framework import serializers

from experiment.models import Experiment


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = "__all__"


class ExperimentDetailSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source="creator.username")

    class Meta:
        model = Experiment
        fields = [
            "id",
            "title",
            "description",
            "status",
            "creator",
            "person_wanted",
            "person_already",
            "money_per_person",
            "money_paid",
            "money_left",
            "time_created",
            "time_modified",
            "activity_location",
            "activity_time",
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
