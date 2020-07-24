from django.urls import path, re_path

from applications.test_projects.apps import TestProjectsConfig
from applications.test_projects.views import TestProjectsView, AddingPageView, ProjectPageView, DeleteProjectView, \
    EditingPageView, NightModeView

app_name = TestProjectsConfig.label

urlpatterns = [
    path("",TestProjectsView.as_view(), name="t_projects"),
    path("adding/", AddingPageView.as_view(), name="adding_page"),
    path("editing/add", AddingPageView.as_view(),name="add"),
    path("id/<str:project_id>/", ProjectPageView.as_view(), name="c_project"),
    path("id/<str:project_id>/delete", DeleteProjectView.as_view(), name="delete"),
    path("id/<str:project_id>/editing", EditingPageView.as_view(), name="editing_page"),
    path("id/<str:project_id>/editing/edit/", EditingPageView.as_view(), name="edit"),
    re_path(".*night_mode", NightModeView.as_view(), name="night_mode")
]