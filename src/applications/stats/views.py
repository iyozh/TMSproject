import datetime

from django.views.generic import TemplateView

from path import COUNTER
from utils.json_utils import get_json
from utils.stats_utils import stats_calculating


class StatsView(TemplateView):
    template_name = "stats/index.html"

    def get_context_data(self):

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

        ctx = {"stats": stats}

        return ctx
