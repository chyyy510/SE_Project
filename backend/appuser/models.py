from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    Group,
    Permission,
)
from django.core.validators import MinValueValidator
from utils.generate_path import GeneratePath
import os
from utils.privacy_protection import PrivacyProtection

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    uid = models.IntegerField(unique=True)
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    salt = models.BinaryField()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # 自定义 related_name，避免与 auth.User.groups 冲突
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # 自定义 related_name，避免与 auth.User.user_permissions 冲突
        blank=True,
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.full_clean()  # 调用验证
        super().save(*args, **kwargs)

    def set_password(self, raw_password):

        self.salt = os.urandom(16)
        self.password = PrivacyProtection.hash_password(raw_password, self.salt)
        # self._password = raw_password

    def check_password(self, raw_password):
        # 使用自定义逻辑验证密码是否正确
        encrypted = PrivacyProtection.hash_password(raw_password, self.salt)
        return self.password == encrypted


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=128)
    avatar = models.ImageField(
        upload_to=GeneratePath.generate_path_avatar,
        default="avatar/user_0/default_avatar.png",
    )
    point = models.IntegerField(
        validators=[MinValueValidator(0)]
    )  # 积分，发布实验时充值，完成实验获取，100:1兑换rmb

    introduction = models.TextField(default="Nothing here.")
