from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission
from .models import Project, Task, RevenueLog

# Unregister the default Group model and register it with your custom settings
admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass

# Optionally, register the User model for easier management of roles
admin.site.unregister(User)
admin.site.register(User, BaseUserAdmin)


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

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='Admin').exists()

    def has_add_permission(self, request):
        return request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Manager').exists()

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='Admin').exists() or request.user.groups.filter(name='Manager').exists()

    def has_view_permission(self, request, obj=None):
        return request.user.groups.filter(name__in=['Admin', 'Manager', 'Viewer']).exists()
