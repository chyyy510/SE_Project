from rest_framework import status
from rest_framework.response import Response
from appuser.models import User
from appuser.serializers import (
    UserSerializer,
    UserRegeisterSerializer,
    UserLoginSerializer,
)

from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .utils import PrivacyProtection


# Create your views here.


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegister(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegeisterSerializer


class UserLogin(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password_hashed = request.data.get("password_hashed")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid email"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        this_password = PrivacyProtection.hash_password(password_hashed, user.salt)

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
        )


class UserTokenRefresh(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
