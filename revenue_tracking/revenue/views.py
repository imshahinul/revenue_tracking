from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, BasePermission
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from .models import Project, Task, RevenueLog
from .serializers import ProjectSerializer, TaskSerializer, RevenueLogSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum


class IsAdminOrManager(BasePermission):
    """
    Custom permission to allow only Admin or Manager to edit objects.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(name='Admin').exists() or
            request.user.groups.filter(name='Manager').exists()
        )

class IsAdmin(BasePermission):
    """
    Custom permission to allow only Admin to delete objects.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Admin').exists()


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]


class RevenueLogViewSet(viewsets.ModelViewSet):
    queryset = RevenueLog.objects.all()
    serializer_class = RevenueLogSerializer
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope, IsAdminOrManager]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['task__project__id', 'task__id', 'date']
    ordering_fields = ['date', 'revenue']

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def project_revenue(self, request):
        project_id = request.query_params.get('project_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not project_id or not start_date or not end_date:
            return Response({"error": "project_id, start_date, and end_date are required."}, status=400)

        logs = RevenueLog.objects.filter(
            task__project__id=project_id,
            date__range=[start_date, end_date]
        ).aggregate(total_revenue=Sum('revenue'))

        return Response({'project_id': project_id, 'total_revenue': logs['total_revenue']})

    def destroy(self, request, *args, **kwargs):
        # Restrict delete functionality to Admin only
        self.permission_classes = [IsAuthenticated, TokenHasReadWriteScope, IsAdmin]
        return super().destroy(request, *args, **kwargs)

