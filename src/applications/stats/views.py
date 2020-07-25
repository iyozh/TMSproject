import datetime

from django.views.generic import TemplateView

from path import COUNTER
from utils.json_utils import get_json
from utils.stats_utils import stats_calculating, visits_counter
from utils.theme_utils import change_mode, get_theme


class StatsView(TemplateView):
    template_name = "stats/index.html"

    def dispatch(self, request, *args, **kwargs):
        visits_counter(self.request.path)
        return super().dispatch(request)

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)

        theme = get_theme(self.request)

        counts = get_json(COUNTER)

        today = datetime.date.today()

        stats = []

        for page in counts:
            stat = {
                "page": page,
                "today": stats_calculating(counts[page], today, 0),
                "yesterday": stats_calculating(
                    counts[page], today - datetime.timedelta(days=1), 0
                ),
                "week": stats_calculating(counts[page], today, 7),
                "month": stats_calculating(counts[page], today, 30),
            }
            stats.append(stat)

        ctx.update({"stats": stats, "theme": theme})

        return ctx

    def post(self, request):
        return change_mode(request, "/stats")
