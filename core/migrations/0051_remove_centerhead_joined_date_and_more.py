# Generated by Django 5.2 on 2025-05-27 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_batch_dailyreport_syllabustopic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='centerhead',
            name='joined_date',
        ),
        migrations.RemoveField(
            model_name='centerhead',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='centerhead',
            name='profile_image',
        ),
    ]
