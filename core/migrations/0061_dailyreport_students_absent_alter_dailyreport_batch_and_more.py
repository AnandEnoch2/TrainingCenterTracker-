# Generated by Django 5.2 on 2025-05-27 12:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_alter_dailyreport_students_present_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyreport',
            name='students_Absent',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='dailyreport',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.batch'),
        ),
        migrations.RemoveField(
            model_name='dailyreport',
            name='students_present',
        ),
        migrations.AlterField(
            model_name='dailyreport',
            name='taught_by',
            field=models.ForeignKey(limit_choices_to={'designation__in': ['trainer', 'Faculty']}, on_delete=django.db.models.deletion.CASCADE, to='core.employee'),
        ),
        migrations.AddField(
            model_name='dailyreport',
            name='students_present',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
