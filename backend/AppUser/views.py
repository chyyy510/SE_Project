from rest_framework import status
from rest_framework.response import Response
from appuser.models import User
from appuser.serializers import (
    UserSerializer,
    DataUserRegisterSerializer,
    DataUserLoginSerializer,
)

from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

import os

from utils.privacy_protection import PrivacyProtection
from utils.generate_info import GenerateInfo


# Create your views here.


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


"""class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegeisterSerializer"""


"""class UserLogin(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password_decrypted = request.data.get("password_hashed")
        password_decrypted = PrivacyProtection.decrypt_password(password_decrypted)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid email"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        this_password = PrivacyProtection.hash_password(password_decrypted, user.salt)

        if user.password_hashed != this_password:
            return Response(
                {"error": "Invalid password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "email": user.email,
                    "nickname": user.nickname,
                    "is_active": user.is_active,
                },
            }
        )"""


class UserTokenRefresh(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserProfileDetail(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({"user": user.username})


class UserProfileAvatarUpload(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        return Response({"user": user.username})


class UserRegister(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = DataUserRegisterSerializer

    def post(self, request, *args, **kwargs):
        # print(request.data)
        email = request.data.get("email")
        user_exists = User.objects.filter(email=email).exists()

        if user_exists:
            return Response(
                {"message": "Email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = request.data.get("username")
        user_exists = User.objects.filter(username=username).exists()

        if user_exists:
            return Response(
                {"message": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # dont exist continue to create
        uid = GenerateInfo.generate_uid()
        salt = os.urandom(16)
        password_encrypted = request.data.get("password_encrypted")
        password_de = PrivacyProtection.decrypt_password(password_encrypted)
        password_hashed = PrivacyProtection.hash_password(password_de, salt)

        user = User(
            uid=uid,
            email=email,
            username=username,
            password_hashed=password_hashed,
            is_active=True,
            is_staff=False,
            salt=salt,
        )

        user.save()

        serializer = UserSerializer(user)

        return Response(serializer.data)
