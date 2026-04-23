from django.contrib import admin
from .models import Department, JobTitle, Employee, Attendance, LeaveType, LeaveRequest, Payroll

admin.site.register(Department)
admin.site.register(JobTitle)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(LeaveType)
admin.site.register(LeaveRequest)
admin.site.register(Payroll)
