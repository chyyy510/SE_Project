from django.db import models
from appuser.models import User
from django.core.validators import MinValueValidator

from decimal import Decimal

# Create your models here.


class Experiment(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    status_choice = {("open", "进行中"), ("close", "已结束")}
    status = models.CharField(max_length=8, choices=status_choice)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    person_wanted = models.IntegerField(validators=[MinValueValidator(1)])  # 需求总数
    person_already = models.IntegerField(validators=[MinValueValidator(0)])  # 已招到
    money_per_person = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    money_paid = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    money_left = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + '"' + self.description + '"'
