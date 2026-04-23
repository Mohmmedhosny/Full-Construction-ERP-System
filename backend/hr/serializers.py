from rest_framework import serializers
from .models import Department, JobTitle, Employee, Attendance, LeaveType, LeaveRequest, Payroll


class DepartmentSerializer(serializers.ModelSerializer):
    head_name = serializers.SerializerMethodField()
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = '__all__'

    def get_head_name(self, obj):
        return obj.head.full_name if obj.head else None

    def get_employee_count(self, obj):
        return obj.employees.filter(status='active').count()


class JobTitleSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = JobTitle
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    job_title_name = serializers.CharField(source='job_title.name', read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeListSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    job_title_name = serializers.CharField(source='job_title.name', read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'first_name', 'last_name', 'full_name', 'email', 'phone',
                  'department', 'department_name', 'job_title', 'job_title_name',
                  'employment_type', 'status', 'hire_date']


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    leave_type_name = serializers.CharField(source='leave_type.name', read_only=True)

    class Meta:
        model = LeaveRequest
        fields = '__all__'


class PayrollSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id_str = serializers.CharField(source='employee.employee_id', read_only=True)

    class Meta:
        model = Payroll
        fields = '__all__'
