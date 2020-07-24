from django.urls import path

from applications.test_projects.apps import TestProjectsConfig
from applications.test_projects.views import TestProjectsView, AddingPageView, ProjectPageView, DeleteProjectView, \
    EditingPageView

app_name = TestProjectsConfig.label

urlpatterns = [
    path("",TestProjectsView.as_view(), name="t_projects"),
    path("adding/", AddingPageView.as_view(), name="adding_page"),
    path("editing/add", AddingPageView.as_view(),name="add"),
    path("id/<str:project_id>/", ProjectPageView.as_view(), name="c_project"),
    path("id/<str:project_id>/delete", DeleteProjectView.as_view(), name="delete"),
    path("id/<str:project_id>/editing", EditingPageView.as_view(), name="editing_page"),
]