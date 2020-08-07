from django.urls import reverse_lazy
from django.views.generic import RedirectView

from applications.test_projects.mixins.single_obj import SingleObject
from applications.test_projects.models import Project


class DeleteProjectView(SingleObject, RedirectView):
    url = reverse_lazy("test_projects:t_projects")
    model = Project

    def get_redirect_url(self, *args, **kwargs):
        project = self.get_object()
        project.delete()
        return super().get_redirect_url()
