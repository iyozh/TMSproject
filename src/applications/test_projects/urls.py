from django.urls import path

from applications.test_projects.apps import TestProjectsConfig
from applications.test_projects.views import (
    DeleteProjectView,
    ProjectPageView,
    TestProjectsView,
)

app_name = TestProjectsConfig.label

urlpatterns = [
    path("", TestProjectsView.as_view(), name="t_projects"),
    path("id/<str:project_id>/", ProjectPageView.as_view(), name="c_project"),
    path("id/<str:project_id>/delete", DeleteProjectView.as_view(), name="delete"),
]
