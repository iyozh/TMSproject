from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from applications.test_projects.models import Project


@admin.register(Project)
class ProjectAdminModel(ModelAdmin):
    pass


