# Generated by Django 5.1.2 on 2024-10-21 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(unique=True)),
                ('nickname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password_hashed', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
            ],
        ),
    ]
