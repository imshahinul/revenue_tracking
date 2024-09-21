from django.test import TestCase
from revenue.models import Project, Task, RevenueLog
from django.utils import timezone
from decimal import Decimal

class ProjectModelTest(TestCase):
    def test_create_project(self):
        project = Project.objects.create(name="Project Alpha", description="A test project")
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(project.name, "Project Alpha")
        self.assertEqual(project.description, "A test project")


class TaskModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Project Alpha", description="A test project")

    def test_create_task(self):
        task = Task.objects.create(project=self.project, name="Task 1", description="First task")
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(task.project.name, "Project Alpha")
        self.assertEqual(task.name, "Task 1")


class RevenueLogModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Project Alpha", description="A test project")
        self.task = Task.objects.create(project=self.project, name="Task 1", description="First task")

    def test_create_revenue_log(self):
        revenue_log = RevenueLog.objects.create(task=self.task, date=timezone.now().date(), revenue=Decimal('100.50'))
        self.assertEqual(RevenueLog.objects.count(), 1)
        self.assertEqual(revenue_log.task.name, "Task 1")
        self.assertEqual(revenue_log.revenue, Decimal('100.50'))
