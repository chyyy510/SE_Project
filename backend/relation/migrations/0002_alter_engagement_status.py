# Generated by Django 5.1.2 on 2024-11-26 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engagement',
            name='status',
            field=models.CharField(choices=[('to-check-result', '实验结果待审核'), ('finish', '已完成'), ('to-qualify-user', '用户资质待审核')], max_length=24),
        ),
    ]
