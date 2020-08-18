from django import forms
from django.views.generic import ListView

from applications.test_projects.models import Project
from utils.stats_utils import count_stats


class AddingForm(forms.Form):
    project_name = forms.CharField(max_length=50)
    started = forms.DateField(required=False)
    ended = forms.DateField(required=False)
    project_description = forms.CharField(max_length=200, required=False)


@count_stats
class TestProjectsView(ListView):
    template_name = "test_projects/projects_template.html"
    queryset = Project.objects.filter(visible=True)


