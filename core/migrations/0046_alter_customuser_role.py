# Generated by Django 5.2 on 2025-05-24 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_centerhead'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('employee', 'Employee'), ('marketingexecutive', 'MarketingExecutive'), ('student', 'Student'), ('centerhead', 'Center Head'), ('admin', 'Admin'), ('telecallers', 'Telecallers'), ('faculty', 'Faculty'), ('dataentry', 'DataEntry')], max_length=20),
        ),
    ]
