from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from core.views import custom_logout
from .views import mark_attendance
from .views import contact_view
from django.views.generic import TemplateView
from .views import centerhead_dashboard
from .views import login_view
from .views import submit_daily_report

urlpatterns = [
    # Login page
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),

    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('marketingexecutive/dashboard/', views.marketingexecutive_dashboard, name='marketingexecutive_dashboard'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),

    # Role-based redirect
    path('redirect/', views.role_redirect, name='role_redirect'),

    # Attendance
    path('attendance/employee/', views.employee_attendance, name='employee_attendance'),
    path('attendance/marketingexecutive/', views.marketingexecutive_attendance, name='marketingexecutive_attendance'),
    path('attendance/student/', views.student_attendance, name='student_attendance'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('attendance-success/', views.attendance_success, name='attendance_success'),

    # Account settings
    path('account/settings/', views.account_settings, name='account_settings'),

    # Admin Dashboard
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Admission-related paths
    path('admission/new/', views.new_admission, name='new_admission'),  # Keep only one path

    # Logout
    path('logout/', custom_logout, name='logout'),

    # Admin Dashboard
    path('admin_dashboard/', views.dashboard, name='admin_dashboard'),

    # Admissions View
    path('admin_dashboard/admissions/', views.Admission, name='admissions'),

    # Marketing Executives View
    path('admin_dashboard/marketing_executives/', views.MarketingExecutive, name='marketing_executives'),

    path('mark_attendance/', mark_attendance, name='mark_attendance'),

    path('attendance/', views.attendance_view, name='attendance'),

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('leave_requests/', views.leave_requests_view, name='leave_requests'),
    path('tasks/', views.tasks_view, name='tasks'),
    path('my-attendance/', views.attendance_history, name='my_attendance'),
    path('contact/', contact_view, name='contact'),
    path('success/', TemplateView.as_view(template_name='success.html'), name='success'),
    path('login/', login_view, name='login'),
    path('centerhead/dashboard/', centerhead_dashboard, name='centerhead_dashboard'),
    path('daily-report/', submit_daily_report, name='submit_daily_report'),
    
    path('admissions/', views.admission_list, name='admission_list'),
]

# For media file handling
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
