from django.views.generic import TemplateView

from utils.stats_utils import count_stats


@count_stats
class ResumeView(TemplateView):
    template_name = "resume/resume.html"
