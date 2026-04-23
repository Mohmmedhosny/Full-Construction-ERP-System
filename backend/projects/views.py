from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum
from .models import Client, Project, Phase, Task, Milestone, ProjectNote
from .serializers import (
    ClientSerializer, ProjectSerializer, ProjectListSerializer,
    PhaseSerializer, PhaseListSerializer, TaskSerializer,
    MilestoneSerializer, ProjectNoteSerializer
)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'contact_person', 'email']
    ordering_fields = ['name', 'created_at']


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.select_related('client', 'project_manager').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'client']
    search_fields = ['name', 'code', 'location', 'description']
    ordering_fields = ['name', 'start_date', 'end_date', 'budget', 'completion_percentage', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        projects = Project.objects.all()
        stats = {
            'total': projects.count(),
            'active': projects.filter(status='active').count(),
            'planning': projects.filter(status='planning').count(),
            'completed': projects.filter(status='completed').count(),
            'on_hold': projects.filter(status='on_hold').count(),
            'total_budget': projects.aggregate(total=Sum('budget'))['total'] or 0,
        }
        return Response(stats)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        project = self.get_object()
        phases = project.phases.all()
        data = {
            'id': project.id,
            'name': project.name,
            'code': project.code,
            'status': project.status,
            'completion_percentage': project.completion_percentage,
            'budget': project.budget,
            'phase_count': phases.count(),
            'task_stats': {
                'total': sum(p.tasks.count() for p in phases),
                'completed': sum(p.tasks.filter(status='completed').count() for p in phases),
                'in_progress': sum(p.tasks.filter(status='in_progress').count() for p in phases),
                'blocked': sum(p.tasks.filter(status='blocked').count() for p in phases),
            }
        }
        return Response(data)


class PhaseViewSet(viewsets.ModelViewSet):
    queryset = Phase.objects.select_related('project').prefetch_related('tasks').all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['project', 'status']
    ordering_fields = ['sequence', 'start_date']

    def get_serializer_class(self):
        if self.action == 'list':
            return PhaseListSerializer
        return PhaseSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('phase', 'phase__project', 'assigned_to').all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['phase', 'status', 'priority', 'assigned_to', 'phase__project']
    search_fields = ['name', 'description']
    ordering_fields = ['due_date', 'priority', 'status', 'created_at']


class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = Milestone.objects.select_related('project').all()
    serializer_class = MilestoneSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['project', 'status']
    ordering_fields = ['date']


class ProjectNoteViewSet(viewsets.ModelViewSet):
    queryset = ProjectNote.objects.select_related('project', 'author').all()
    serializer_class = ProjectNoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
