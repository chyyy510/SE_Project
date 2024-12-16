from rest_framework import serializers
from relation.models import Engagement, Tags


class EngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engagement
        fields = "__all__"


class EngagementCreateSerializer(serializers.Serializer):
    class Meta:
        model = Engagement
        fileds = ["experiment"]


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"
