# Generated by Django 5.2 on 2025-04-21 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_delete_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='designation',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='phone',
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='employeetask',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=50),
        ),
    ]
