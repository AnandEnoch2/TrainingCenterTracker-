# Generated by Django 5.2 on 2025-05-27 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_remove_centerhead_joined_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='students',
            field=models.ManyToManyField(related_name='student_batches', to='core.student'),
        ),
    ]
