# Generated by Django 5.2 on 2025-05-27 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0059_student_total_fees_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyreport',
            name='students_present',
            field=models.ManyToManyField(related_name='daily_attendance', to='core.student'),
        ),
        migrations.AlterField(
            model_name='dailyreport',
            name='taught_by',
            field=models.ForeignKey(limit_choices_to={'role__in': ['trainer', 'Faculty']}, on_delete=django.db.models.deletion.CASCADE, to='core.employee'),
        ),
    ]
