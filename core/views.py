from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import CustomUser, Student, MarketingExecutive, Course, CenterHead

# --- Login View ---
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        print(f"Attempt login: {username}")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print(f"Authenticated as: {user.username} with role: {user.role}")
            login(request, user)

            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'employee':
                return redirect('employee_dashboard')
            elif user.role == 'centerhead':
                return redirect('centerhead_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'marketingexecutive':
                return redirect('marketingexecutive_dashboard')
            else:
                messages.error(request, 'Invalid role.')
                return redirect('login')
        else:
            print("❌ Authentication failed.")
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'core/login.html')



# --- Dashboard view (Admin or shared) ---
from django.shortcuts import render
from .models import Admission, Course, Student

def dashboard(request):
    # Calculate the counts
    admissions_count = Admission.objects.count()
    courses_count = Course.objects.count()
    students_count = Student.objects.count()

    # Fetch data for the students and admissions tables
    students = Student.objects.all()
    admissions = Admission.objects.all()

    context = {
        'admissions_count': admissions_count,
        'courses_count': courses_count,
        'students_count': students_count,
        'students': students,
        'admissions': admissions,
    }

    return render(request, 'core/dashboard.html', context)

# --- Attendance views ---
@login_required
def employee_attendance(request):
    if request.user.role != 'employee':
        return redirect('unauthorized')
    return render(request, 'attendance/employee_form.html')

@login_required
def marketingexecutive_attendance(request):
    if request.user.role != 'marketingexecutive':
        return redirect('unauthorized')
    return render(request, 'attendance/marketingexecutive_form.html')

@login_required
def student_attendance(request):
    if request.user.role != 'student':
        return redirect('unauthorized')
    return render(request, 'attendance/student_form.html')


@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('unauthorized')
    return render(request, 'core/admin_dashboard.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def centerhead_dashboard(request):
    if request.user.role != 'centerhead':
        return redirect('unauthorized')
    return render(request, 'core/centerhead_dashboard.html')


# --- Role-based Dashboard Views ---
@login_required
def student_dashboard(request):
    return render(request, 'core/student_dashboard.html')



@login_required
def employee_dashboard(request):
    return render(request, 'core/employee_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')
@login_required
def centerhead_dashboard(request):
    return render(request, 'core/centerhead_dashboard.html')

# --- Optional: Role-based redirect view (not used in login but can be reused) ---
@login_required
def role_redirect(request):
    user = request.user
    if user.role == 'student':
        return redirect('student_dashboard')
    if user.role == 'centerhead':
        return redirect('centerhead_dashboard')

    elif user.role == 'marketingexecutive':
        return redirect('marketingexecutive_dashboard')
    elif user.role == 'employee':
        return redirect('employee_dashboard')
    elif user.role == 'admin':
        return redirect('admin_dashboard')
    else:
        return redirect('login')  # fallback


from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Admission

@login_required
def centerhead_dashboard(request):
    if request.user.role == 'centerhead':
        admissions = Admission.objects.all().order_by('-admission_date')
        return render(request, 'core/centerhead_dashboard.html', {
            'admissions': admissions
        })
    else:
        return redirect('unauthorized')  # define this URL or view accordingly



# views.py
from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    if request.user.is_authenticated:
        request.user.is_online = False  # Mark as offline
        request.user.save()
    logout(request)
    return redirect('login')  # Or your preferred redirect


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Attendance, EmployeeTask
from .utils import get_location_name  # Ensure you have the correct import for this

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        location_str = request.POST.get('location', '')  # Might be empty or not provided
        if location_str:
            location_name = location_str  # Directly use the provided location string
        else:
            location_name = "Head Office "  # Default when no location is provided

        # Create a new attendance entry with the location name and status (True for attendance)
        Attendance.objects.create(
            user=request.user,
            location=location_name,
            status=True
        )

        # Optionally, update the EmployeeTask
        employee_task = EmployeeTask.objects.filter(user=request.user).first()
        if employee_task:
            employee_task.status = 'Attendance Marked'
            employee_task.save()

        # Redirect to the success page after marking attendance
        return redirect('attendance_success')

    # Redirect to employee dashboard if the request is not POST (for example, on page load)
    return redirect('employee_dashboard')

def attendance_success(request):
    attendances = Attendance.objects.filter(user=request.user)
    return render(request, 'attendance/employee_form.html', {'attendances': attendances})


# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Attendance

@login_required
def attendance_history(request):
    user_attendance = Attendance.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'core/employee_dashboard.html', {'user_attendance': user_attendance})


from django.contrib.auth.decorators import login_required

@login_required
def employee_dashboard(request):
    if request.method == 'POST' and 'task_description' in request.POST:
        task_desc = request.POST['task_description']
        status = request.POST['status']

        # Create task assigned to current user without due_date
        EmployeeTask.objects.create(
            user=request.user,
            task_desc=task_desc,
            status=status
        )

        # Mark attendance for the current user on task submission
        Attendance.objects.create(
            user=request.user,
            location="Head Office",
            status=True
        )

        return redirect('employee_dashboard')

    tasks = EmployeeTask.objects.filter(user=request.user)
    user_attendance = Attendance.objects.filter(user=request.user).order_by('-date', '-time')

    for attendance in user_attendance:
        attendance.display_location = "Head Office"

    return render(request, 'core/employee_dashboard.html', {
        'tasks': tasks,
        'user_attendance': user_attendance,
    })




# Account settings
    
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

@login_required
def account_settings(request):
    user = request.user
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Account updated successfully!')
        return redirect('account_settings')

    return render(request, 'core/account_settings.html', {'user': user})

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

@login_required
def account_settings(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if new_password1 or new_password2:
            if new_password1 == new_password2:
                user.set_password(new_password1)
                update_session_auth_hash(request, user)  # Prevent logout
                messages.success(request, "Password updated successfully.")
            else:
                messages.error(request, "Passwords do not match.")
                return redirect('account_settings')  # or wherever your settings page is

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('account_settings')

    return render(request, 'core/account_settings.html')
      

# Marketing executive

# views.py
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import F
from .models import Student, Admission, Course, MarketingExecutive
from django.contrib.auth.decorators import login_required

@login_required
def new_admission(request):
    if request.method == "POST":
        student_name = request.POST.get("student_name")
        student_email = request.POST.get("student_email")
        course_id = request.POST.get("course_id")
        admission_date = request.POST.get("admission_date") or timezone.now().date()
        amount_paid = request.POST.get("amount_paid")

        # Validate amount_paid and convert to Decimal
        from decimal import Decimal, InvalidOperation
        try:
            amount_paid = Decimal(amount_paid)
        except (InvalidOperation, TypeError):
            amount_paid = Decimal('0.00')

        # Associate marketing executive if logged-in user has one
        marketing_exec = None
        if hasattr(request.user, 'marketingexecutive'):
            marketing_exec = request.user.marketingexecutive

        # Get the Course object
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return render(request, "attendance/new_admission.html", {
                "error": "Invalid course ID.",
                "today_date": timezone.now().date(),
                "courses": Course.objects.all()
            })

        # Check if student exists by email
        student, created = Student.objects.get_or_create(
            email=student_email,
            defaults={'name': student_name, 'enrolled_course': course}
        )

        if not created:
            # Student exists, update total_fees_paid (add amount_paid)
            # Make sure Student model has total_fees_paid field
            if hasattr(student, 'total_fees_paid'):
                from django.db.models import F
                student.total_fees_paid = F('total_fees_paid') + amount_paid
                student.save(update_fields=['total_fees_paid'])
                # Refresh from db to get updated value
                student.refresh_from_db()
            else:
                # If no total_fees_paid field, you may want to add it
                pass

        # Pull center from logged-in user (if available)
        center_value = getattr(request.user, 'center', None)

        # Create Admission record linked to the student
        Admission.objects.create(
            student=student,
            course=course,
            marketing_executive=marketing_exec,
            admission_date=admission_date,
            amount_paid=amount_paid,
            status='active',
            center=center_value
        )

        # Update marketing executive stats
        if marketing_exec:
            marketing_exec.admissions_worked_on += 1
            marketing_exec.total_admissions += 1
            marketing_exec.admission_rate = (
                (marketing_exec.admissions_worked_on / marketing_exec.total_admissions) * 100
            )
            marketing_exec.save()

        return redirect("dashboard")

    # GET request - render admission form
    courses = Course.objects.all()
    today = timezone.now().date()
    return render(request, "attendance/new_admission.html", {
        "courses": courses,
        "today_date": today
    })

# Marketing Executives
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Admission, MarketingExecutive,EmployeeTask
from django.utils import timezone
from datetime import timedelta

@login_required
def marketingexecutive_dashboard(request):
    user = request.user

    try:
        marketing_executive = MarketingExecutive.objects.get(user=user)
    except MarketingExecutive.DoesNotExist:
        return render(request, 'core/error_page.html', {'message': 'You are not authorized.'})

    # ✅ First get all admissions
    all_admissions = Admission.objects.filter(marketing_executive=marketing_executive)

    # ✅ Then prepare for recent admissions
    recent_admissions = all_admissions.order_by('-admission_date')[:5]

    # ✅ Basic calculations
    admission_count = all_admissions.count()
    target_admissions = 20
    incentive_per_admission = 500

    incentive_earned = admission_count * incentive_per_admission
    bonus = 2000 if admission_count >= target_admissions else 0
    bonus_status = "Eligible" if bonus else "Pending"

    progress_percentage = (admission_count / target_admissions) * 100 if target_admissions > 0 else 0

    # ✅ Now safely prepare data for graph
    today = timezone.now().date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]  # 6 days ago to today
    admissions_per_day = []

    for day in last_7_days:
        count = all_admissions.filter(admission_date=day).count()  # Fixed no __date
        admissions_per_day.append(count)

    # ✅ Task handling
    tasks = EmployeeTask.objects.filter(user=user)

    if request.method == 'POST':
        task_text = request.POST.get('task')
        if task_text:
            EmployeeTask.objects.create(user=user, task_desc=task_text)
            return redirect('marketingexecutive_dashboard')  # Reload the page after adding task

    # ✅ Pass everything to context
    context = {
        'admission_count': admission_count,
        'incentive_earned': incentive_earned,
        'bonus': bonus,
        'bonus_status': bonus_status,
        'admissions': recent_admissions,
        'progress_percentage': progress_percentage,
        'target_admissions': target_admissions,
        'last_7_days': [day.strftime('%b %d') for day in last_7_days],  # formatted dates
        'admissions_per_day': admissions_per_day,  # admission counts
        'tasks': tasks,  # Add tasks to context
    }

    return render(request, 'core/marketingexecutive_dashboard.html', context)


# Ensure the admin can access this page
# Admin views
# views.py

from django.shortcuts import render
from .models import Student, Course, Admission, Attendance, LoginRecord, EmployeeAttendance, MarketingExecutiveAttendance, StudentAttendance
from django.utils.timezone import now, timedelta

def admin_dashboard(request):
    today = now().date()
    week_ago = today - timedelta(days=7)

    # Logins
    total_logins = LoginRecord.objects.count()
    today_logins = LoginRecord.objects.filter(login_time__date=today).count()

    # Attendance
    employee_attendance_count = EmployeeAttendance.objects.filter(date=today, status='Present').count()
    marketing_executive_attendance_count = MarketingExecutiveAttendance.objects.filter(date=today, status='Present').count()
    student_attendance_count = StudentAttendance.objects.filter(date=today, status='Present').count()

    # Admissions
    total_admissions = Admission.objects.count()
    weekly_admissions = Admission.objects.filter(admission_date__gte=week_ago).count()

    # Context
    context = {
        'total_logins': total_logins,
        'today_logins': today_logins,
        'employee_attendance_count': employee_attendance_count,
        'marketing_executive_attendance_count': marketing_executive_attendance_count,
        'student_attendance_count': student_attendance_count,
        'total_admissions': total_admissions,
        'weekly_admissions': weekly_admissions,
    }

    return render(request, 'core/admin_dashboard.html', context)



# core/views.py

from django.shortcuts import render

def attendance_view(request):
    return render(request, 'core/attendance.html')


def leave_requests_view(request):
    return render(request, 'core/leave_requests.html')

def tasks_view(request):
    return render(request, 'core/tasks.html')

#Contact Form
from django.shortcuts import render
from .forms import ContactForm

def contact_view(request):
    submitted = False  # Track whether form was submitted
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            submitted = True  # Set flag to true
    else:
        form = ContactForm()

    return render(request, 'core/login.html', {'form': form, 'submitted': submitted})




from django.shortcuts import render
from .models import Admission, DailyReport, Batch, Employee
from django.contrib.auth.decorators import login_required

@login_required
def submit_daily_report(request):
    message = ''
    admissions = Admission.objects.all()
    faculty_list = Employee.objects.filter(designation__in=['trainer', 'Faculty'])

    if request.method == 'POST':
        batch_name = request.POST.get('batch')
        topic_covered = request.POST.get('topic_covered')
        students_present = request.POST.get('students_present_count')
        students_absent = request.POST.get('students_absent_count')
        taught_by_id = request.POST.get('taught_by')

        if not (batch_name and topic_covered and students_present and students_absent and taught_by_id):
            message = '❌ Please fill in all the fields.'
        else:
            try:
                batch = Batch.objects.get(name=batch_name)
                employee = Employee.objects.get(id=taught_by_id)

                DailyReport.objects.create(
                    batch=batch,
                    topic_covered=topic_covered,
                    students_present=int(students_present),
                    students_absent=int(students_absent),
                    taught_by=employee
                )
                message = '✅ Report submitted successfully.'

            except Batch.DoesNotExist:
                message = f"❌ Batch '{batch_name}' not found."
            except Employee.DoesNotExist:
                message = "❌ Selected faculty not found."
            except Exception as e:
                message = f"❌ Error: {str(e)}"

    return render(request, 'core/centerhead_dashboard.html', {
        'message': message,
        'admissions': admissions,
        'faculty_list': faculty_list
    })


from django.shortcuts import render
from .models import Admission
from django.contrib.auth.decorators import login_required

@login_required
def admission_list(request):
    admissions = Admission.objects.all().order_by('-admission_date')  # newest first (optional)
    return render(request, 'core/centerhead_dashboard.html', {
        'admissions': admissions
    })
