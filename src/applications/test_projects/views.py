import os
from typing import NamedTuple

from django import forms
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.base import RedirectView

from path import PROJECTS
from utils.json_utils import get_json, save_data
from utils.stats_utils import count_stats


class AddingForm(forms.Form):
    project_name = forms.CharField(max_length=50)
    project_date = forms.CharField(max_length=50)
    project_description = forms.CharField(max_length=200)


@count_stats
class TestProjectsView(FormView):
    template_name = "test_projects/projects_template.html"
    success_url = reverse_lazy("test_projects:t_projects")
    form_class = AddingForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        projects_content = get_json(PROJECTS)
        projects = []

        for id in projects_content:
            project = {
                "project_id": id,
                "project_name": projects_content[id]["project_name"],
                "project_date": projects_content[id]["project_date"],
                "project_description": projects_content[id]["project_description"],
            }
            projects.append(project)

        ctx.update({"projects": projects})

        return ctx

    def form_valid(self, form):
        projects = get_json(PROJECTS)
        new_project = {}
        project_id = os.urandom(16).hex()
        new_project[project_id] = {
            "project_name": form.cleaned_data["project_name"],
            "project_date": form.cleaned_data["project_date"],
            "project_description": form.cleaned_data["project_description"],
        }
        projects.update(new_project)
        save_data(PROJECTS, projects)
        return super().form_valid(form)


class EditingForm(forms.Form):
    project_name = forms.CharField(max_length=50)
    project_date = forms.CharField()
    project_description = forms.CharField(max_length=200)


class ProjectPageView(FormView):
    template_name = "test_projects/c_project.html"
    form_class = EditingForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        projects = get_json(PROJECTS)

        project_id = self.kwargs["project_id"]

        certain_project = projects[project_id]

        ctx.update({"certain_project": certain_project, "project_id": project_id})

        return ctx

    def form_valid(self, form):
        projects = get_json(PROJECTS)
        project_id = self.kwargs["project_id"]
        projects[project_id] = {}
        projects[project_id].update(form.cleaned_data)
        save_data(PROJECTS, projects)
        return super().form_valid(form)

    def get_initial(self, **kwargs):
        project = self.build_project()
        ready_project = project._asdict()
        return ready_project

    def build_project(self):
        project_id = self.kwargs["project_id"]
        projects = get_json(PROJECTS)
        return ProjectData(
            project_name=projects[project_id]["project_name"],
            project_date=projects[project_id]["project_date"],
            project_description=projects[project_id]["project_description"],
        )

    def get_success_url(self):
        project_id = self.kwargs["project_id"]
        success_url = reverse_lazy(
            "test_projects:c_project", kwargs={"project_id": project_id}
        )
        return success_url


class DeleteProjectView(RedirectView):
    url = reverse_lazy("test_projects:t_projects")

    def get_redirect_url(self, *args, **kwargs):
        projects = get_json(PROJECTS)
        project_id = self.kwargs["project_id"]
        projects.pop(project_id)
        save_data(PROJECTS, projects)
        return super().get_redirect_url()


class ProjectData(NamedTuple):
    project_name: str
    project_date: str
    project_description: str


#
