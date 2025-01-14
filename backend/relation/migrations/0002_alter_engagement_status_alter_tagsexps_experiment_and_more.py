# Generated by Django 5.1.4 on 2024-12-16 11:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0001_initial'),
        ('relation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engagement',
            name='status',
            field=models.CharField(choices=[('to-qualify-user', '用户资质待审核'), ('finish', '已完成'), ('to-check-result', '实验结果待审核')], max_length=24),
        ),
        migrations.AlterField(
            model_name='tagsexps',
            name='experiment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='experiment.experiment'),
        ),
        migrations.AlterField(
            model_name='tagsexps',
            name='tags',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='relation.tags'),
        ),
    ]
