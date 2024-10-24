# Generated by Django 5.1.2 on 2024-10-24 15:27

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appuser', '0002_user_salt_alter_user_password_hashed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('status', models.CharField(max_length=8)),
                ('person_wanted', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('person_already', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('money_per_person', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('money_paid', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('money_left', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appuser.user')),
            ],
        ),
    ]
