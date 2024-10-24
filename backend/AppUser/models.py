from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.


class User(models.Model):
    uid = models.IntegerField(unique=True)
    nickname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hashed = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    salt = models.BinaryField()

    def __str__(self):
        return self.nickname
