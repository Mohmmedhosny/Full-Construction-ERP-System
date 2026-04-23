from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, JobTitleViewSet, EmployeeViewSet, AttendanceViewSet, LeaveTypeViewSet, LeaveRequestViewSet, PayrollViewSet

router = DefaultRouter()
router.register('departments', DepartmentViewSet)
router.register('job-titles', JobTitleViewSet)
router.register('employees', EmployeeViewSet)
router.register('attendance', AttendanceViewSet)
router.register('leave-types', LeaveTypeViewSet)
router.register('leave-requests', LeaveRequestViewSet)
router.register('payroll', PayrollViewSet)

urlpatterns = router.urls
