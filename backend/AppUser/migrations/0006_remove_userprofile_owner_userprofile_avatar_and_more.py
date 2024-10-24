# Generated by Django 5.1.2 on 2024-10-24 16:25

import django.db.models.deletion
import utils.generate_path
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0005_alter_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='owner',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='avatar/user_0/default_avatar.png', upload_to=utils.generate_path.GeneratePath.generate_path_avatar),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='appuser.user'),
            preserve_default=False,
        ),
    ]
