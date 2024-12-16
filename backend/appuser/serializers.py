from rest_framework import serializers
from appuser.models import User, UserProfile, DataUserRegister, DataUserLogin


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "uid",
            "username",
            "email",
            "password",
            "is_active",
            "is_staff",
        ]


class UserUsernameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username"]


class UserProfileNicknameSerializer(serializers.Serializer):
    class Meta:
        model = UserProfile
        fields = ["nickname"]


class UserProfileAvatarSerializer(serializers.Serializer):
    class Meta:
        model = UserProfile
        fields = ["avatar"]


class DataUserRegisterSerializer(serializers.Serializer):
    class Meta:
        model = DataUserRegister
        fields = ["email", "username", "password_encrypted"]


class DataUserLoginSerializer(serializers.Serializer):
    class Meta:
        model = DataUserLogin
        fields = ["email", "password_encrypted"]
