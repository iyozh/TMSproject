from django.urls import path

from applications.projects.views import ProjectsView

from .apps import ProjectsConfig

app_name = ProjectsConfig.label

urlpatterns = [path("", ProjectsView.as_view(), name="projects_view")]
