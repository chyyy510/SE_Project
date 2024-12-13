from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from appuser.models import User, UserProfile
from appuser.serializers import (
    UserSerializer,
    DataUserRegisterSerializer,
    DataUserLoginSerializer,
)

from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import AnonymousUser
from django.conf import settings


from utils.privacy_protection import PrivacyProtection
from utils.generate_info import GenerateInfo
from utils.generate_path import GeneratePath


# Create your views here.


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class UserList(generics.ListAPIView):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    pagination_class = UserPagination


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
        # salt = os.urandom(16)
        password_encrypted = request.data.get("password_encrypted")
        password_de = PrivacyProtection.decrypt_password(password_encrypted)

        # password_hashed = PrivacyProtection.hash_password(password_de, salt)

        user = User(
            uid=uid,
            email=email,
            username=username,
            # password_hashed=password_hashed,
            is_active=True,
            is_staff=False,
            # salt=salt,
        )

        user.set_password(password_de)

        user.save()

        userprofile = UserProfile(user=user, nickname="user" + str(uid))
        userprofile.save()

        serializer = UserSerializer(user)

        return Response(serializer.data)


class UserLogin(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = DataUserLoginSerializer

    def post(self, request, *args, **kwargs):
        # print("login ok")
        print(request.data)
        email = request.data.get("email")
        password_decrypted = request.data.get("password_encrypted")
        password_decrypted = PrivacyProtection.decrypt_password(password_decrypted)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid email"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        print("email right")

        if user.check_password(password_decrypted) == False:
            return Response(
                {"error": "Invalid password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        print("pwd right")

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "email": user.email,
                    "username": user.username,
                    "is_active": user.is_active,
                },
            }
        )


class UserTokenRefresh(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # user = request.user
        # print(user)
        return super().post(request, *args, **kwargs)


class UserProfileDetail(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        profile = UserProfile.objects.get(user=user)

        return Response(
            {
                "user": user.username,
                "nickname": profile.nickname,
                "avatar": profile.avatar,  # TODO:返回图片好像要额外注意些东西
            },
            status=status.HTTP_200_OK,
        )


class UserProfileAvatarUpload(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        image = request.FILES.get("avatar")

        if not image:
            return Response(
                {"detail": "No avatar file uploaded."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not image.content_type.startswith("image"):
            return Response(
                {"detail": "The file is not an image."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # 设置文件存储位置
        filename = GeneratePath.generate_path_avatar(request, image.name)
        filename = fs.save(filename, image)  # 保存文件
        file_url = fs.url(filename)

        profile = UserProfile.objects.get(user=user)
        profile.avatar = file_url

        profile.save()

        return Response({"user": user.username, "avatar_url": file_url})
