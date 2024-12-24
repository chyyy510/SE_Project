from rest_framework import serializers
from relation.models import Engagement, Tags, TagsExps

from appuser.serializers import UserAndUserProfileSerializer


class EngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engagement
        fields = "__all__"


class EngagementCreateSerializer(serializers.Serializer):
    class Meta:
        model = Engagement
        fileds = ["experiment"]


class VolunteerListSerializer(serializers.ModelSerializer):
    user = UserAndUserProfileSerializer()

    class Meta:
        model = Engagement
        fields = ["user", "status"]


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"


class TagsExpsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagsExps
        fields = "__all__"
