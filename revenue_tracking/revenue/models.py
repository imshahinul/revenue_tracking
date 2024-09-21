from django.db import models
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('project', 'name')

    def __str__(self):
        return f"{self.project.name} - {self.name}"


class RevenueLog(models.Model):
    task = models.ForeignKey(Task, related_name='revenue_logs', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('task', 'date')

    def __str__(self):
        return f"{self.task.name} - {self.date} - ${self.revenue}"