from django.views.generic import TemplateView

from utils.stats_utils import visits_counter


class ProjectsView(TemplateView):
    template_name = "projects/projects.html"

    def dispatch(self, request, *args, **kwargs):
        visits_counter(self.request.path)
        return super().dispatch(request)
