from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project, Phase, Task, Milestone, ProjectNote


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    assigned_to_detail = UserSerializer(source='assigned_to', read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class PhaseSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Phase
        fields = '__all__'

    def get_task_count(self, obj):
        return obj.tasks.count()


class PhaseListSerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Phase
        fields = ['id', 'project', 'name', 'sequence', 'start_date', 'end_date', 'status', 'completion_percentage', 'budget', 'task_count']

    def get_task_count(self, obj):
        return obj.tasks.count()


class ProjectNoteSerializer(serializers.ModelSerializer):
    author_detail = UserSerializer(source='author', read_only=True)

    class Meta:
        model = ProjectNote
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    client_detail = ClientSerializer(source='client', read_only=True)
    project_manager_detail = UserSerializer(source='project_manager', read_only=True)
    phases = PhaseListSerializer(many=True, read_only=True)
    milestones = MilestoneSerializer(many=True, read_only=True)
    phase_count = serializers.SerializerMethodField()
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_phase_count(self, obj):
        return obj.phases.count()

    def get_task_count(self, obj):
        return sum(phase.tasks.count() for phase in obj.phases.all())


class ProjectListSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    project_manager_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'code', 'client', 'client_name', 'project_manager', 'project_manager_name',
                  'location', 'start_date', 'end_date', 'status', 'priority', 'budget', 'completion_percentage']

    def get_project_manager_name(self, obj):
        if obj.project_manager:
            return f"{obj.project_manager.first_name} {obj.project_manager.last_name}".strip() or obj.project_manager.username
        return None
