from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum
from .models import Department, JobTitle, Employee, Attendance, LeaveType, LeaveRequest, Payroll
from .serializers import (
    DepartmentSerializer, JobTitleSerializer,
    EmployeeSerializer, EmployeeListSerializer,
    AttendanceSerializer, LeaveTypeSerializer,
    LeaveRequestSerializer, PayrollSerializer
)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'code']


class JobTitleViewSet(viewsets.ModelViewSet):
    queryset = JobTitle.objects.select_related('department').all()
    serializer_class = JobTitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department']


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('department', 'job_title').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'status', 'employment_type']
    search_fields = ['first_name', 'last_name', 'employee_id', 'email']
    ordering_fields = ['last_name', 'hire_date', 'base_salary']

    def get_serializer_class(self):
        if self.action == 'list':
            return EmployeeListSerializer
        return EmployeeSerializer

    @action(detail=False, methods=['get'])
    def stats(self, request):
        employees = Employee.objects.all()
        return Response({
            'total': employees.count(),
            'active': employees.filter(status='active').count(),
            'on_leave': employees.filter(status='on_leave').count(),
            'by_department': list(
                employees.values('department__name').annotate(count=Count('id'))
            ),
            'by_type': list(
                employees.values('employment_type').annotate(count=Count('id'))
            ),
        })


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('employee', 'project').all()
    serializer_class = AttendanceSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['employee', 'status', 'date', 'project']
    ordering_fields = ['date']

    @action(detail=False, methods=['get'])
    def today(self, request):
        from django.utils import timezone
        today = timezone.now().date()
        attendance = Attendance.objects.filter(date=today).select_related('employee')
        serializer = self.get_serializer(attendance, many=True)
        return Response(serializer.data)


class LeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.select_related('employee', 'leave_type').all()
    serializer_class = LeaveRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['employee', 'status', 'leave_type']
    ordering_fields = ['start_date', 'created_at']

    @action(detail=False, methods=['get'])
    def pending(self, request):
        requests = LeaveRequest.objects.filter(status='pending').select_related('employee', 'leave_type')
        serializer = self.get_serializer(requests, many=True)
        return Response(serializer.data)


class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.select_related('employee').all()
    serializer_class = PayrollSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['employee', 'status']
    ordering_fields = ['period_end', 'net_salary']

    def perform_create(self, serializer):
        payroll = serializer.validated_data
        gross = (
            payroll.get('base_salary', 0) +
            payroll.get('overtime_pay', 0) +
            payroll.get('allowances', 0) +
            payroll.get('bonuses', 0)
        )
        net = gross - payroll.get('tax_deduction', 0) - payroll.get('other_deductions', 0)
        serializer.save(
            created_by=self.request.user,
            gross_salary=gross,
            net_salary=net
        )

    @action(detail=False, methods=['get'])
    def summary(self, request):
        data = Payroll.objects.filter(status='paid').aggregate(
            total_gross=Sum('gross_salary'),
            total_net=Sum('net_salary'),
            total_tax=Sum('tax_deduction'),
        )
        return Response(data)
