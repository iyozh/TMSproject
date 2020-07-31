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
    path("id/<str:pk>/", ProjectPageView.as_view(), name="c_project"),
    path("id/<str:pk>/delete", DeleteProjectView.as_view(), name="delete"),
]
