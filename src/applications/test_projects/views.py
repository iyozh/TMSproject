import os

from django import forms
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.views.generic.base import View

from utils.json_utils import get_json, save_data

from path import PROJECTS


class TestProjectsView(TemplateView):
    template_name = "test_projects/projects_template.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        projects_content = get_json(PROJECTS)
        projects = []

        for id in projects_content:
            project = {
                "project_id": id,
                "project_name": projects_content[id]["project_name"],
                "project_date": projects_content[id]["project_date"],
                "project_description": projects_content[id]["project_description"]
            }
            projects.append(project)

        ctx.update({"projects": projects})

        return ctx


class AddingForm(forms.Form):
    project_name = forms.CharField(max_length=50)
    project_date = forms.CharField()
    project_description = forms.CharField(max_length=200)


class AddingPageView(FormView):
    template_name = "test_projects/add_projects.html"
    success_url = "/test_projects"
    form_class = AddingForm

    def form_valid(self, form):
        projects = get_json(PROJECTS)
        new_project = {}
        project_id = os.urandom(16).hex()
        new_project[project_id] = {
            "project_name": form.cleaned_data["project_name"],
            "project_date": form.cleaned_data["project_date"],
            "project_description": form.cleaned_data["project_description"]
        }
        projects.update(new_project)
        save_data(PROJECTS, projects)
        return super().form_valid(form)


class ProjectPageView(TemplateView):
    template_name = "test_projects/c_project.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        projects = get_json(PROJECTS)

        project_id = kwargs["project_id"]

        certain_project = projects[project_id]

        ctx.update({"certain_project": certain_project,"project_id":project_id})

        return ctx


class DeleteProjectView(View):

    def post(self,request, **kwargs):
        projects = get_json(PROJECTS)
        project_id = kwargs["project_id"]
        projects.pop(project_id)
        save_data(PROJECTS, projects)
        return redirect("/test_projects")


class EditingForm(forms.Form):
    project_name = forms.CharField(max_length=50)
    project_date = forms.CharField()
    project_description = forms.CharField(max_length=200)


class EditingPageView(FormView):
    template_name = "test_projects/edit_projects.html"
    success_url = ""
    form_class = EditingForm

    def form_valid(self, form):
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        return ctx

    def get_initial(self,**kwargs):
        project_id = kwargs["project_id"]
        projects = get_json(PROJECTS)
        project_name = projects[project_id]["project_name"]
        project_date = projects[project_id]["project_date"]
        project_description = projects[project_id]["project_description"]
        return {
            "project_name": project_name,
            "project_date": project_date,
            "project_description": project_description
        }