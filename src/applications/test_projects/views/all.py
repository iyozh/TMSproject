from django import forms
from django.urls import reverse_lazy
from django.views.generic import FormView

from applications.test_projects.models import Project
from utils.stats_utils import count_stats


class AddingForm(forms.Form):
    project_name = forms.CharField(max_length=50)
    started = forms.DateField(required=False)
    ended = forms.DateField(required=False)
    project_description = forms.CharField(max_length=200, required=False)


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
