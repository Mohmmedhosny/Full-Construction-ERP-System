from django.contrib import admin
from .models import Client, Project, Phase, Task, Milestone, ProjectNote

admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Phase)
admin.site.register(Task)
admin.site.register(Milestone)
admin.site.register(ProjectNote)
