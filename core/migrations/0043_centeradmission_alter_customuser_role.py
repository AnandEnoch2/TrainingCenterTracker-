# Generated by Django 5.2 on 2025-05-24 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_remove_admission_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='CenterAdmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('center_name', models.CharField(max_length=100)),
                ('center_address', models.TextField(blank=True, null=True)),
                ('course_name', models.CharField(max_length=100)),
                ('course_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('batch_name', models.CharField(max_length=100)),
                ('batch_start_date', models.DateField()),
                ('batch_end_date', models.DateField(blank=True, null=True)),
                ('student_name', models.CharField(max_length=100)),
                ('student_email', models.EmailField(max_length=254)),
                ('admission_date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('completed', 'Completed')], default='active', max_length=20)),
                ('total_fees_paid', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fees_payment_log', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('employee', 'Employee'), ('marketingexecutive', 'MarketingExecutive'), ('student', 'Student'), ('center_head', 'Center Head'), ('admin', 'Admin'), ('telecallers', 'Telecallers'), ('faculty', 'Faculty'), ('dataentry', 'DataEntry')], max_length=20),
        ),
    ]
