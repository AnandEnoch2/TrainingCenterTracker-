from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Define the Course model
class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=50)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    incharge = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'employee'}  # Only employees can be incharge
    )

    mode = models.CharField(
        max_length=20,
        choices=[('online', 'Online'), ('offline', 'Offline'), ('hybrid', 'Hybrid')],
        default='offline'
    )

    certificate_provided = models.BooleanField(default=False)
    max_students = models.PositiveIntegerField(default=30)


    def __str__(self):
        return self.name
    






# Define the marketing model
from django.db import models
from django.conf import settings  # Ensure settings is imported

class MarketingExecutive(models.Model):
    # Linking to the custom user model via settings.AUTH_USER_MODEL
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    
    # Target and other performance-related details
    target_achieved = models.IntegerField(default=0)  # Number of targets achieved
    target_set = models.IntegerField(default=10)  # Number of targets set for the executive
    incentives = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Incentives earned
    
    # Admission details that they worked on
    admissions_worked_on = models.IntegerField(default=0)
    total_admissions = models.IntegerField(default=0)
    admission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # Admission success rate

    # Status of the marketing executive (active/inactive)
    is_active = models.BooleanField(default=True)

    # Date of joining
    date_joined = models.DateField(auto_now_add=True)

    # Any additional notes about the executive
    notes = models.TextField(blank=True, null=True)

    # Track salary details if necessary
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Base salary
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Bonus or extra earnings

    def __str__(self):
        return f"{self.name} ({self.email})"
    
    class Meta:
        verbose_name = 'Marketing Executive'
        verbose_name_plural = 'Marketing Executives'



# Define the Student model
class Student(models.Model):
    # existing fields
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    enrolled_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_fees_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    @property
    def admission_centers(self):
        # Returns a list of unique centers from all admissions
        return list(self.admission_set.values_list('center', flat=True).distinct())

    @property
    def latest_admission_center(self):
        latest_adm = self.admission_set.order_by('-admission_date').first()
        return latest_adm.center if latest_adm else None


# Define the Employee model
class Employee(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    def __str__(self):
        return self.name
    


# Login based on role

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('marketingexecutive', 'MarketingExecutive'),
        ('student', 'Student'),
        ('centerhead', 'CenterHead'),
        ('admin', 'Admin'),
        ('telecallers', 'Telecallers'),
        ('faculty','Faculty'),
        ('dataentry','DataEntry')

    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    # Add this field to track Online/Offline status
    is_online = models.BooleanField(default=False)
    location = models.CharField(max_length=100, blank=True, null=True) 
    center = models.CharField(max_length=100, null=True, blank=True)




from django.conf import settings

class EmployeeTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Link to the custom user model
    task_description = models.TextField()
    status = models.CharField(max_length=255)
    due_date = models.DateField(null=True, blank=True) 

    def __str__(self):
        return self.task_description





# Attendance model
from django.conf import settings
from django.db import models

class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, blank=True, null=True)
    center = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Auto-fill role and center from user if not set
        if not self.role and hasattr(self.user, 'role'):
            self.role = self.user.role
        if not self.center and hasattr(self.user, 'center'):
            self.center = self.user.center
        super().save(*args, **kwargs)

class Admission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marketing_executive = models.ForeignKey('MarketingExecutive', on_delete=models.SET_NULL, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    admission_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('completed', 'Completed')], default='active')
    center = models.CharField(max_length=100, blank=True, null=True)

    def get_marketing_executive_name(self):
        return self.marketing_executive.name if self.marketing_executive else "Center Head"
    get_marketing_executive_name.short_description = 'Marketing Executive'

    def __str__(self):
        return f"Student: {self.student.name}, Course: {self.course.name}"


#Admin dashboard
from django.shortcuts import render
from .models import Student, Course, Admission, Attendance
from django.utils.timezone import now

def admin_dashboard(request):
    # Fetch students, courses, and admissions
    students = Student.objects.all()
    courses = Course.objects.all()
    admissions = Admission.objects.all()

    today = now().date()

    # Calculate
    total_logins = LoginRecord.objects.count()
    today_logins = LoginRecord.objects.filter(login_time__date=today).count()

    employee_attendance_count = Attendance.objects.filter(date=today, status='Present').count()
    marketing_executive_attendance_count = MarketingExecutiveAttendance.objects.filter(date=today, status='Present').count()
    student_attendance_count = StudentAttendance.objects.filter(date=today, status='Present').count()

    total_admissions = admissions.count()

    student_admission_count = {student.id: Admission.objects.filter(student=student).count() for student in students}

    # Context
    context = {
        'students': students,
        'courses': courses,
        'admissions': admissions,
        'total_logins': total_logins,
        'today_logins': today_logins,
        'employee_attendance_count': employee_attendance_count,
        'marketing_executive_attendance_count': marketing_executive_attendance_count,
        'student_attendance_count': student_attendance_count,
        'total_admissions': total_admissions,
    }
    return render(request, 'dashboard.html', context)


# Tasks
from django.db import models
from django.conf import settings
import datetime
from django.utils import timezone

class EmployeeTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_desc = models.CharField(max_length=255)  # note: different field name here
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    def get_user_role(self):
        return self.user.role

    def get_user_location(self):
        return self.user.location



# core/models.py
from django.db import models

class BonusReport(models.Model):
    marketing_executive = models.ForeignKey('MarketingExecutive', on_delete=models.CASCADE)
    date = models.DateField()
    total_bonus = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Bonus Report for {self.marketing_executive} on {self.date}"




# user login time

from django.db import models
from django.conf import settings

class UserLogin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)  # Automatically set the login time

    def __str__(self):
        return f"{self.user.username} logged in at {self.login_time}"



#ATTENDANCE MODELS
from django.conf import settings
from django.db import models

# 1. Login Record
class LoginRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)

# 2. Employee Attendance
class EmployeeAttendance(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

# 3. Marketing Executive Attendance
from django.db import models
from django.contrib.auth.models import User  # or your custom user

class MarketingExecutiveAttendance(models.Model):
    executive = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    date = models.DateField()
    status = models.CharField(max_length=10, choices=(('Present', 'Present'), ('Absent', 'Absent')))

    def __str__(self):
        return f"{self.executive.username} - {self.date} - {self.status}"


# 4. Student Attendance
class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])


def attendance_view(request):
    return render(request, 'core/attendance.html')


from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


from django.db import models

class CenterAdmission(models.Model):
    # Center details
    center_name = models.CharField(max_length=100)
    centerhead_name = models.CharField(max_length=100, default='Center Head')
    center_address = models.TextField(blank=True, null=True)

    # Course details
    course_name = models.CharField(max_length=100)
    course_fee = models.DecimalField(max_digits=10, decimal_places=2)

    # Batch details
    batch_name = models.CharField(max_length=100)
    batch_start_date = models.DateField()
    batch_end_date = models.DateField(blank=True, null=True)

    # Student details
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField()

    # Admission details
    admission_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('active','Active'), ('completed','Completed')], default='active')

    # Fees logs (you can store total fees paid or multiple payments as JSON/text)
    total_fees_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fees_payment_log = models.TextField(blank=True, null=True)  # e.g. JSON string storing payment history

    def __str__(self):
        return f"{self.student_name} - {self.course_name} ({self.center_name})"


class CenterHead(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    center_name = models.CharField(max_length=100)
    center_address = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.user.username} - {self.center_name}"

class SyllabusTopic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)


class DailyReport(models.Model):
    batch = models.ForeignKey('Batch', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    topic_covered = models.CharField(max_length=255)
    taught_by = models.ForeignKey('Employee', on_delete=models.CASCADE, limit_choices_to={'designation__in': ['trainer', 'Faculty']})
    students_present = models.PositiveIntegerField(default=0)
    students_absent = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.date} - {self.batch.name}"

        

from django.db import models
from django.conf import settings

class Batch(models.Model):
    name = models.CharField(max_length=100)
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    students = models.ManyToManyField('core.Student', related_name='student_batches', blank=True)


    def __str__(self):
        return f"{self.name} - {self.course_name}"
