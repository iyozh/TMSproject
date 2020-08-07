from django import forms
from django.urls import reverse_lazy
from django.views.generic import FormView

from applications.test_projects.mixins.single_obj import SingleObject
from applications.test_projects.models import Project
from utils.utils import asdict


class EditingForm(forms.Form):
    project_name = forms.CharField(max_length=50)
    started = forms.DateField(required=False)
    ended = forms.DateField(required=False)
    project_description = forms.CharField(max_length=200, required=False)


class ProjectPageView(SingleObject, FormView):
    template_name = "test_projects/c_project.html"
    form_class = EditingForm
    model = Project

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        certain_project = self.get_object()
        dct = asdict(certain_project)
        ctx.update({"certain_project": dct})

        return ctx

    def form_valid(self, form):
        project = self.get_object()
        self.update_object(project, form)
        project.save()
        return super().form_valid(form)

    def get_initial(self, **kwargs):
        certain_project = self.get_object()
        dct = asdict(certain_project)
        return dct

    def get_success_url(self):
        pk = self.get_object_id()
        success_url = reverse_lazy("test_projects:c_project", kwargs={"pk": pk})
        return success_url
