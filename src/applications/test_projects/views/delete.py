from django.urls import reverse_lazy
from django.views.generic import DeleteView, RedirectView

from applications.test_projects.mixins.single_obj import SingleObject
from applications.test_projects.models import Project


class DeleteProjectView(DeleteView):
    success_url = reverse_lazy("test_projects:t_projects")
    model = Project
