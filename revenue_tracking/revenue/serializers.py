from rest_framework import serializers
from .models import Project, Task, RevenueLog

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class RevenueLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueLog
        fields = '__all__'
