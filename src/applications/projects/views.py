from django.views.generic import TemplateView

from utils.stats_utils import count_stats


@count_stats
class ProjectsView(TemplateView):
    template_name = "projects/projects.html"
