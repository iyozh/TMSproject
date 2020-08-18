from django.urls import reverse_lazy
from django.views.generic import CreateView

from applications.test_projects.models import Project
from utils.stats_utils import count_stats


@count_stats
class AddProjectView(CreateView):
    model = Project
    fields = ["name", "started", "ended", "description", "visible"]
