from django.contrib import admin

# Register your models here.
from .models import Project, Server, Service, Permission

admin.site.register(Permission)

@admin.register(Project)
class ServerAdmin(admin.ModelAdmin):
    list_display = ['name', 'env']
    list_filter = ['env']

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ['ip', 'project_name', 'project_env']
    list_filter = ['project__name', 'project__env']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'server_project', 'server_env', 'server_ip', 'service_version', 'charcater']
    list_filter = ['server__project__name', 'server__project__env']
