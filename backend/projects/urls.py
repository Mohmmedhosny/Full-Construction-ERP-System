from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ProjectViewSet, PhaseViewSet, TaskViewSet, MilestoneViewSet, ProjectNoteViewSet

router = DefaultRouter()
router.register('clients', ClientViewSet)
router.register('projects', ProjectViewSet)
router.register('phases', PhaseViewSet)
router.register('tasks', TaskViewSet)
router.register('milestones', MilestoneViewSet)
router.register('notes', ProjectNoteViewSet)

urlpatterns = router.urls
