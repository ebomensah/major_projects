# Generated by Django 5.1.5 on 2025-03-01 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='first_time_login',
            field=models.BooleanField(default=True),
        ),
    ]
