# Generated by Django 5.2 on 2025-04-21 11:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_marketingexecutive_delete_trainer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeetask',
            name='due_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
