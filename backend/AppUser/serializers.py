from rest_framework import serializers
from appuser.models import User
from appuser.utils import GenerateInfo
import os
from .utils import PrivacyProtection


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "uid",
            "nickname",
            "email",
            "password_hashed",
            "is_active",
            "is_staff",
        ]


class UserRegeisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "nickname", "password_hashed"]

    def create(self, validated_data):
        validated_data["uid"] = GenerateInfo.generate_uid()
        validated_data["is_active"] = True  # ?TODO:需要发送验证码激活吗
        validated_data["is_staff"] = False

        validated_data["salt"] = os.urandom(16)
        validated_data["password_hashed"] = PrivacyProtection.hash_password(
            validated_data["password_hashed"], validated_data["salt"]
        )

        return super().create(validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password_hashed"]
