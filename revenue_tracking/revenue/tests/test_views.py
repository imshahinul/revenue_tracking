from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from revenue.models import Project, Task, RevenueLog
from decimal import Decimal
from django.utils import timezone

class ProjectAPITest(APITestCase):
    def test_create_project(self):
        url = reverse('project-list')  # Uses router-defined URL
        data = {'name': 'Project Alpha', 'description': 'A test project'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(Project.objects.get().name, 'Project Alpha')

    def test_get_projects(self):
        Project.objects.create(name="Project Alpha", description="A test project")
        url = reverse('project-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Project Alpha")


class TaskAPITest(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Project Alpha", description="A test project")

    def test_create_task(self):
        url = reverse('task-list')
        data = {'project': self.project.id, 'name': 'Task 1', 'description': 'First task'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().name, 'Task 1')

    def test_get_tasks(self):
        Task.objects.create(project=self.project, name="Task 1", description="First task")
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Task 1')


class RevenueLogAPITest(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Project Alpha", description="A test project")
        self.task = Task.objects.create(project=self.project, name="Task 1", description="First task")

    def test_create_revenue_log(self):
        url = reverse('revenuelog-list')
        data = {'task': self.task.id, 'date': timezone.now().date(), 'revenue': '100.50'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RevenueLog.objects.count(), 1)
        self.assertEqual(RevenueLog.objects.get().revenue, Decimal('100.50'))

    def test_get_revenue_logs(self):
        RevenueLog.objects.create(task=self.task, date=timezone.now().date(), revenue=Decimal('100.50'))
        url = reverse('revenuelog-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['revenue'], '100.50')