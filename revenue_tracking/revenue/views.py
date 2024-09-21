from rest_framework import viewsets
from .models import Project, Task, RevenueLog
from .serializers import ProjectSerializer, TaskSerializer, RevenueLogSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class RevenueLogViewSet(viewsets.ModelViewSet):
    queryset = RevenueLog.objects.all()
    serializer_class = RevenueLogSerializer
