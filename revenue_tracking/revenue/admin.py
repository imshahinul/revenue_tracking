from django.contrib import admin
from .models import Project, Task, RevenueLog

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('project', 'name')
    list_filter = ('project',)


@admin.register(RevenueLog)
class RevenueLogAdmin(admin.ModelAdmin):
    list_display = ('task', 'date', 'revenue')
    list_filter = ('task', 'date')
    search_fields = ('task__name',)