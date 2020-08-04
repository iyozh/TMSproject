import os
from dataclasses import asdict
from typing import NamedTuple

from django import forms
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.base import RedirectView

from applications.test_projects.mixins.single_obj import SingleObject
from applications.test_projects.models import Project
from path import PROJECTS
from utils.json_utils import get_json, save_data
from utils.stats_utils import count_stats


class AddingForm(forms.Form):
    project_name = forms.CharField(max_length=50)
    started = forms.DateField()
    ended = forms.DateField()
    project_description = forms.CharField(max_length=200)


@count_stats
class TestProjectsView(FormView):
    template_name = "test_projects/projects_template.html"
    success_url = reverse_lazy("test_projects:t_projects")
    form_class = AddingForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        projects = Project.objects.all()
        ctx.update({"projects": projects})

        return ctx

    def form_valid(self, form):
        project = Project(**form.cleaned_data)
        project.save()
        return super().form_valid(form)


class EditingForm(forms.Form):
    project_name = forms.CharField(max_length=50)
    started = forms.DateField()
    ended = forms.DateField()
    project_description = forms.CharField(max_length=200)


class ProjectPageView(SingleObject, FormView):
    template_name = "test_projects/c_project.html"
    form_class = EditingForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        certain_project = self.get_object()
        dct = {
            "pk": certain_project.pk,
            "project_name": certain_project.project_name,
            "started": certain_project.started,
            "ended": certain_project.ended,
            "project_description": certain_project.project_description,
        }
        ctx.update({"certain_project": dct})

        return ctx

    def form_valid(self, form):
        project = self.get_object()
        self.update_object(project, form)
        project.save()
        return super().form_valid(form)

    def get_initial(self, **kwargs):
        certain_project = self.get_object()
        dct = {
            "project_name": certain_project.project_name,
            "started": certain_project.started,
            "ended": certain_project.ended,
            "project_description": certain_project.project_description,
        }
        return dct

    # def build_project(self):
    #     project_id = self.kwargs["pk"]
    #     projects = get_json(PROJECTS)
    #     return ProjectData(
    #         project_name=projects[project_id]["project_name"],
    #         started=projects[project_id]["started"],
    #         ended=projects[project_id]["ended"],
    #         project_description=projects[project_id]["project_description"],
    #     )

    def get_success_url(self):
        pk = self.get_object_id()
        success_url = reverse_lazy("test_projects:c_project", kwargs={"pk": pk})
        return success_url


class DeleteProjectView(SingleObject, RedirectView):
    url = reverse_lazy("test_projects:t_projects")

    def get_redirect_url(self, *args, **kwargs):
        project = self.get_object()
        project.delete()
        return super().get_redirect_url()


class ProjectData(NamedTuple):
    project_name: str
    started: str
    ended: str
    project_description: str


#
