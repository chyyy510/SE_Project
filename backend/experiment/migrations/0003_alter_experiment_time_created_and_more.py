# Generated by Django 5.1.2 on 2024-11-13 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0002_searchkeyword_alter_experiment_money_left_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='time_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
