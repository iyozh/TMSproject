from django import forms
from django.views.generic import DetailView

from applications.test_projects.models import Project


class EditingForm(forms.Form):
    name = forms.CharField(max_length=50)
    started = forms.DateField(required=False)
    ended = forms.DateField(required=False)
    description = forms.CharField(max_length=200, required=False)


class ProjectPageView(DetailView):
    template_name = "test_projects/c_project.html"
    model = Project

