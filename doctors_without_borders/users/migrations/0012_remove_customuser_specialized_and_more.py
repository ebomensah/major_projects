# Generated by Django 5.1.5 on 2025-02-25 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_customuser_specialized_profile_recent_labs_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='specialized',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='profile_picture',
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile_pics/'),
        ),
        migrations.AddField(
            model_name='doctorhistory',
            name='specialized',
            field=models.CharField(blank=True, choices=[('Specialist', 'Specialist'), ('Medical Officer', 'MO'), ('Consultant', 'Consultant')], max_length=50, null=True),
        ),
    ]
