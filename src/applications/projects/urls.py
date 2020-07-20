from django.urls import path
from .apps import ProjectsConfig
from applications.projects.views import ProjectsView

app_name = ProjectsConfig.label

urlpatterns = [
    path("", ProjectsView.as_view(), name='projects_view')
]