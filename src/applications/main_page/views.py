from django.views.generic import TemplateView

from utils.stats_utils import count_stats


@count_stats
class MainPageView(TemplateView):
    template_name = "main_page/index.html"
