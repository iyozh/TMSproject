from django.views.generic import UpdateView

from applications.test_projects.models import Project


class UpdateProjectView(UpdateView):
    model = Project
    fields = ["name", "started", "ended", "description", "visible"]
    template_name_suffix = "_update_form"
