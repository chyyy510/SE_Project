from rest_framework import serializers
from appuser.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "uid",
            "nickname",
            "email",
            "password_hashed",
            "is_active",
            "is_staff",
        ]
