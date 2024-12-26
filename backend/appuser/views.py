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

from utils.payment import Payment

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


class UserPay(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = request.user

        amount = request.data.get("amount")  # TODO:积分数吧，限制为整数

        if not amount.isdigit():
            return Response(
                {"detail": "Amount must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        amount = int(amount)
        if amount <= 0:
            return Response(
                {"detail": "Invalid amount. 金额不合法。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 直接支付成功，point增加
        profile = UserProfile.objects.get(user=user)
        profile.point += amount
        profile.save()

        return Response(
            {"message": "Pay successfully. 成功充值。"}, status=status.HTTP_200_OK
        )

        # 以下是调用支付宝接口，暂时不管TODO:

        """order_id = GenerateInfo.generate_trade_no(user.id)

        try:
            pay_url = Payment.create_recharge_order(
                amount=amount / 100, order_id=order_id
            )
        except:
            return Response(
                {"detail": "Payment error. 支付出错。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "Redirecting to Alipay payment page"},
            status=302,
            headers={"Location": pay_url},
        )"""


class UserPayCallback(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        return Response("success")  # 必须返回 'success'，否则支付宝会重试回调


"""        data = request.POST.dict()  # 接收支付宝 POST 数据

        # 验证签名
        if not Payment.handle_alipay_callback(data):
            return Response("fail")  # 签名验证失败，返回 'fail'
        # 签名验证通过，处理具体业务逻辑
        trade_status = data.get("trade_status")  # 获取交易状态
        order_id = data.get("out_trade_no")  # 获取订单号

        if trade_status == "TRADE_SUCCESS":
            # 交易支付成功，更新订单状态为已支付
            print(f"订单 {order_id} 支付成功！")
            # TODO: 更新数据库订单状态
        elif trade_status == "TRADE_FINISHED":
            # 交易已完成，不可退款
            print(f"订单 {order_id} 交易已完成！")
            # TODO: 处理完成状态的订单逻辑
        elif trade_status == "WAIT_BUYER_PAY":
            # 交易创建，等待买家付款
            print(f"订单 {order_id} 等待付款")
        elif trade_status == "TRADE_CLOSED":
            # 交易关闭
            print(f"订单 {order_id} 已关闭！")
        else:
            print(f"订单 {order_id} 未知状态: {trade_status}")

        return Response("success")  # 必须返回 'success'，否则支付宝会重试回调
"""


class UserCashOut(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        log_print(request.headers, request.data)
        if isinstance(request.user, AnonymousUser):
            return Response(
                {"detail": "Authentication required. 该功能需要先登录。"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = request.user

        amount = request.data.get("amount")  # TODO:积分数吧，限制为整数

        if not amount.isdigit():
            return Response(
                {"detail": "Amount must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        amount = int(amount)
        if amount <= 0:
            return Response(
                {"detail": "Invalid amount. 金额不合法。"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 直接成功
        profile = UserProfile.objects.get(user=user)
        if amount > profile.point:
            return Response(
                {"detail": "Invalid amount. 金额不合法。"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        profile.point -= amount
        profile.save()

        return Response(
            {"message": "Cash out successfully. 成功提现。"}, status=status.HTTP_200_OK
        )
