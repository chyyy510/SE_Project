from rest_framework import serializers
from appuser.models import User, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "uid",
            "username",
            "email",
            "is_active",
            "is_staff",
        ]


class UserUsernameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username"]


class UsernameStatusSerializer(serializers.Serializer):
    username = serializers.CharField()
    status = serializers.CharField


class UserProfileNicknameSerializer(serializers.Serializer):
    class Meta:
        model = UserProfile
        fields = ["nickname"]


class UserProfileAvatarSerializer(serializers.Serializer):
    class Meta:
        model = UserProfile
        fields = ["avatar"]
