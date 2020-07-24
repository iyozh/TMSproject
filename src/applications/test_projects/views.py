import os

from django import forms
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.views.generic.base import View

from utils.json_utils import get_json, save_data

from path import PROJECTS
from utils.theme_utils import get_theme, change_mode


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
        theme = get_theme(self.request)
        ctx.update({"projects": projects, "theme": theme})

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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        theme = get_theme(self.request)
        ctx.update({"theme":theme})
        return ctx


class ProjectPageView(TemplateView):
    template_name = "test_projects/c_project.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        projects = get_json(PROJECTS)

        project_id = kwargs["project_id"]

        certain_project = projects[project_id]

        theme = get_theme(self.request)

        ctx.update({"certain_project": certain_project, "project_id": project_id,"theme": theme})

        return ctx


class DeleteProjectView(View):

    def post(self, request, **kwargs):
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
    form_class = EditingForm

    def form_valid(self, form):
        # project_name = form.cleaned_data["project_name"]
        # project_date = form.cleaned_data["project_date"]
        # project_description = form.cleaned_data["project_description"]
        projects = get_json(PROJECTS)
        project_id = self.kwargs["project_id"]
        for item in form.cleaned_data:
            projects[project_id][item] = form.cleaned_data[item]
        save_data(PROJECTS,projects)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        project_id = self.kwargs["project_id"]
        theme = get_theme(self.request)
        ctx.update({"project_id": project_id, "theme":theme})
        return ctx

    def get_initial(self, **kwargs):
        project_name, project_date, project_description = self.build_project()
        return {
            "project_name": project_name,
            "project_date": project_date,
            "project_description": project_description
        }

    def build_project(self):
        project_id = self.kwargs["project_id"]
        projects = get_json(PROJECTS)
        project_name = projects[project_id]["project_name"]
        project_date = projects[project_id]["project_date"]
        project_description = projects[project_id]["project_description"]

        return project_name, project_date, project_description

    def get_success_url(self):
        project_id = self.kwargs["project_id"]
        success_url = f"/test_projects/id/{project_id}"
        return success_url

class NightModeView(View):

    def post(self,request):
        path = self.request.path
        new_path = path.replace("/night_mode","")
        return change_mode(self.request, new_path)
