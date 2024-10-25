from django.db import models
from utils.generate_path import GeneratePath

# Create your models here.


class User(models.Model):
    uid = models.IntegerField(unique=True)
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    password_hashed = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    salt = models.BinaryField()

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=128)
    avatar = models.ImageField(
        upload_to=GeneratePath.generate_path_avatar,
        default="avatar/user_0/default_avatar.png",
    )


# 以下为前后端数据传输时用的字段，不存储与数据库中
class DataUserRegister(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=128, unique=True)
    password_encrypted = models.CharField(max_length=1024)

    class Meta:
        managed = False


class DataUserLogin(models.Model):
    email = models.EmailField()
    password_encrypted = models.CharField(max_length=1024)

    class Meta:
        managed = False
