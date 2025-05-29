from django.contrib import admin
from .models import (
    Course,
    Student,
    Employee,
    MarketingExecutive,
    CustomUser,
    Attendance,
    Admission,
    EmployeeTask,
    ContactMessage,

)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration','fee','incharge','mode','max_students')
    search_fields = ('name',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'enrolled_course','latest_admission_center')
    search_fields = ('name', 'email')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'email', 'phone')
    search_fields = ('name', 'email', 'designation')

@admin.register(MarketingExecutive)
class MarketingExecutiveAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact_number', 'is_active', 'target_achieved')
    search_fields = ('name', 'email')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_online', 'center', 'is_active')
    list_filter = ('role', 'is_online', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'location','center', 'status','role')
    list_filter = ('status', 'date')
    search_fields = ('user__username',)



from django.contrib import admin
from .models import Admission

class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'get_marketing_executive_name','center', 'amount_paid', 'admission_date', 'status']

    def get_marketing_executive_name(self, obj):
        return obj.get_marketing_executive_name()

    get_marketing_executive_name.short_description = 'Marketing Executive'

admin.site.register(Admission, AdmissionAdmin)

@admin.register(EmployeeTask)
class EmployeeTaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_role', 'user_location', 'task_desc', 'status', 'created_at')

    def user_role(self, obj):
        return obj.user.role
    user_role.short_description = 'Role'  # column header in admin

    def user_location(self, obj):
        return obj.user.location
    user_location.short_description = 'Location'


@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'message','email', 'created_at')
    search_fields = ('name',)

from django.contrib import admin
from .models import CenterAdmission, CenterHead

@admin.register(CenterAdmission)
class CenterAdmissionAdmin(admin.ModelAdmin):
    list_display = (
        'student_name', 'student_email',
        'course_name', 'center_name',
        'batch_name', 'admission_date', 'total_fees_paid', 'status'
    )
    search_fields = ('student_name', 'student_email', 'course_name', 'center_name')
    list_filter = ('center_name', 'course_name', 'status')


from django.contrib import admin
from .models import CenterHead

@admin.register(CenterHead)
class CenterHeadAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_role', 'center_name', 'center_address')  # only these fields

    readonly_fields = ()  # remove 'joined_date' if not present in model

    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_name.short_description = 'Name'

    def get_role(self, obj):
        return getattr(obj.user, 'role', 'CenterHead')
    get_role.short_description = 'Role'


from django.contrib import admin
from .models import Batch

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'course_name', 'start_date', 'end_date', 'get_students')
    search_fields = ('name', 'course_name')
    filter_horizontal = ('students',)

    def get_students(self, obj):
        return ", ".join([str(student) for student in obj.students.all()])
    get_students.short_description = 'Students'


from django.contrib import admin
from .models import DailyReport

class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'batch', 'topic_covered', 'taught_by', 'students_present', 'students_absent')
    list_filter = ('date', 'batch', 'taught_by')
    search_fields = ('batch__batch_name', 'topic_covered', 'taught_by__username')  # assuming 'batch_name' is field in Batch

admin.site.register(DailyReport, DailyReportAdmin)
