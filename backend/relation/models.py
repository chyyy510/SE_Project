from django.db import models
from appuser.models import User
from experiment.models import Experiment


# Create your models here.
class Engagement(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # TODO:
    experiment = models.ForeignKey(
        Experiment, on_delete=models.SET_NULL, null=True
    )  # TODO:
    status_choice = {
        ("to-qualify-user", "用户资质待审核"),
        ("to-check-result", "实验结果待审核"),
        ("finish", "已完成"),
    }
    status = models.CharField(max_length=24, choices=status_choice)
