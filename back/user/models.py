from django.db import models

# Create your models here.

class Users(models.Model):
    email = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    password_encrypted = models.CharField(max_length=30, blank=True, null=True)