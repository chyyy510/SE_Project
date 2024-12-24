from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from appuser.models import User, UserProfile
from appuser.serializers import UserSerializer

from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import AnonymousUser
from django.conf import settings


from utils.privacy_protection import PrivacyProtection
from utils.generate_info import GenerateInfo
from utils.generate_path import GeneratePath
from utils.log_print import log_print


# Create your views here.


# pagination
class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class UserUsernamePagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100


# view
class UserList(generics.ListAPIView):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    pagination_class = UserPagination

    def get(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
        return super().get(request, *args, **kwargs)


# 通过username查找用户，返回email+用户主页信息
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
        username = request.GET.get("username", "")
        try:
            user = User.objects.get(username=username)
        except Exception:
            return Response(
                {"detail": "User doesn't exist. 该用户不存在。"},
                status=status.HTTP_404_NOT_FOUND,
            )

        profile = UserProfile.objects.get(user=user)

        log_print(profile.avatar)

        response = Response(
            {
                "message": "Find the user successfully. 成功找到该用户。",
                "email": user.email,
                "username": username,
                "nickname": profile.nickname,
                "avatar": profile.avatar.url,
                "point": profile.point,
                "introduction": profile.introduction,
            },
            status=status.HTTP_200_OK,
        )

        return response


class UserRegister(generics.GenericAPIView):
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
        email = request.data.get("email")
        user_exists = User.objects.filter(email=email).exists()

        if user_exists:
            return Response(
                {"detail": "Email already exists. 邮箱已存在。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = request.data.get("username")
        user_exists = User.objects.filter(username=username).exists()

        if user_exists:
            return Response(
                {"detail": "Username already exists. 用户名已存在。"},
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

        try:
            user.save()
        except Exception:
            return Response(
                {"detail": "Format error. 有内容不符合格式。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        userprofile = UserProfile(user=user, nickname="user" + str(uid), point=0)
        userprofile.save()

        serializer = UserSerializer(user)

        return Response(serializer.data)


class UserLogin(generics.GenericAPIView):
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        log_print(request.headers, request.data)

        email = request.data.get("email")
        password_decrypted = request.data.get("password_encrypted")
        password_decrypted = PrivacyProtection.decrypt_password(password_decrypted)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid email. 邮箱不存在。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.check_password(password_decrypted) == False:
            return Response(
                {"detail": "Invalid password. 密码错误。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)

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
        log_print(request.headers, request.data)
        try:
            response = super().post(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"detail": "Token is invalid or expired. 令牌无效或已过期。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response.data["message"] = "Access token has been refreshed. access令牌已更新。"

        return response


# TODO:可能不再需要，或者再修改成别的功能
class UserProfileDetail(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
        user = request.user
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        profile = UserProfile.objects.get(user=user)

        return Response(
            {
                "user": user.username,
                "nickname": profile.nickname,
                "avatar": profile.avatar.url,
            },
            status=status.HTTP_200_OK,
        )


class UserProfileAvatarUpload(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
        user = request.user
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        image = request.FILES.get("avatar")

        if not image:
            return Response(
                {"detail": "No avatar file uploaded. 未上传头像文件。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not image.content_type.startswith("image"):
            return Response(
                {"detail": "The file is not an image. 该文件不是图片。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # 设置文件存储位置
        filename = GeneratePath.generate_path_avatar(request, image.name)
        filename = fs.save(filename, image)  # 保存文件
        file_url = fs.url(filename).replace(settings.MEDIA_URL, "", 1)
        log_print(file_url)

        profile = UserProfile.objects.get(user=user)
        profile.avatar = file_url

        profile.save()

        return Response({"user": user.username, "avatar": file_url})


class UserProfileEdit(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = request.user

        try:
            if (
                username := request.data.get("username")
            ) is not None:  # TODO:不能修改和重复
                log_print("username:", username)
                user.username = username
                user.save()
            if (email := request.data.get("email")) is not None:  # TODO:不能修改和重复
                log_print("email:", email)
                user.email = email
                user.save()
            if (introduction := request.data.get("introduction")) is not None:
                log_print("introduction:", introduction)

                profile = UserProfile.objects.get(user=user)
                profile.introduction = introduction
                profile.save()
            if (
                new_password_encrypted := request.data.get("new_password_encrypted")
            ) is not None:
                log_print("new_pwd:", new_password_encrypted)
                old_password_encrypted = request.data.get("old_password_encrypted")
                if old_password_encrypted is None:
                    log_print("old_pwd:", old_password_encrypted)
                    return Response(
                        {"detail": "Please enter old password. 请输入旧密码。"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                old_password_decrypted = PrivacyProtection.decrypt_password(
                    old_password_encrypted
                )
                if not user.check_password(old_password_decrypted):
                    return Response(
                        {"detail": "Password is wrong. 旧密码错误。"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                user.set_password(
                    PrivacyProtection.decrypt_password(new_password_encrypted)
                )
                user.save()
            serializer = UserSerializer(user)
            response = Response(serializer.data)

            response.data["message"] = (
                "User profile edited successfully. 用户信息更新成功。"
            )

            return response

        except Exception:
            return Response(
                {"detail": "Format error. 有内容不符合格式。"},
                status=status.HTTP_400_BAD_REQUEST,
            )
