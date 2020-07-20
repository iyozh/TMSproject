import datetime

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from path import COUNTER, TABLE_TEMPLATE, TABLE_PAGES, TABLE_COUNTS, PORTFOLIO
from utils.stats_utils import visits_counter, stats_calculating
from utils.file_utils import get_content
from utils.json_utils import get_json



class StatsView(TemplateView):
    template_name = "stats/index.html"

    def get_context_data(self):
        counts = get_json(COUNTER)

        today = datetime.date.today()

        stats = []

        for page in counts:
            stat = {"page": page,
                     "today": stats_calculating(counts[page], today, 0),
                     "yesterday": stats_calculating(
                         counts[page], today - datetime.timedelta(days=1), 0
                     ),
                     "week": stats_calculating(counts[page], today, 7),
                     "month": stats_calculating(counts[page], today, 30)
                     }
            stats.append(stat)

        ctx = {
            "stats": stats
        }

        return ctx
