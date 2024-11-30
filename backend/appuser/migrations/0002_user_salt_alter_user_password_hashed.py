# Generated by Django 5.1.2 on 2024-10-24 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='salt',
            field=models.BinaryField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='password_hashed',
            field=models.CharField(max_length=128),
        ),
    ]