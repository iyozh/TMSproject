import datetime

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from path import COUNTER, TABLE_TEMPLATE, TABLE_PAGES, TABLE_COUNTS, PORTFOLIO
from utils.stats_utils import visits_counter, stats_calculating
from utils.file_utils import get_content
from utils.json_utils import get_json


def get_stats(request):
    visits_counter(request.path)
    counts = get_json(COUNTER)

    today = datetime.date.today()

    stats = {}

    for page in counts:
        stats[page] = {}
        stats[page]["today"] = stats_calculating(counts[page], today, 0)
        stats[page]["yesterday"] = stats_calculating(
            counts[page], today - datetime.timedelta(days=1), 0
        )
        stats[page]["week"] = stats_calculating(counts[page], today, 7)
        stats[page]["month"] = stats_calculating(counts[page], today, 30)

    table_template = get_content(TABLE_TEMPLATE)
    for page, visits in stats.items():
        table_template += get_content(TABLE_PAGES).format(page=page)
        for date, count in visits.items():
            table_template += get_content(TABLE_COUNTS).format(count=count)

    file_name = PORTFOLIO / "stats" / "index.html"
    content = get_content(file_name).format(stats=table_template)
    return HttpResponse(content)