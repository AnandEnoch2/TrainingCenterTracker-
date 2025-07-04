# Generated by Django 5.2 on 2025-05-13 07:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import datetime
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_attendance_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeetask',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='employeetask',
            name='due_date',
            field=models.DateField(default=datetime.date.today),  # or some other date
        ),
        migrations.AlterField(
            model_name='employeetask',
            name='status',
            field=models.CharField(max_length=255),
        ),
    ]
