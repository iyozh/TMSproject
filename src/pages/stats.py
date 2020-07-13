import datetime

from django.http import HttpResponse

from utils.file_utils import get_content
from utils.json_utils import get_json, save_data
from path import (COUNTER, PORTFOLIO, TABLE_COUNTS, TABLE_PAGES,
                      TABLE_TEMPLATE)


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


def visits_counter(path):
    counts = get_json(COUNTER)
    today = str(datetime.date.today())

    if path not in counts:
        counts[path] = {}
    if today not in counts[path]:
        counts[path][today] = 0
    counts[path][today] += 1
    save_data(COUNTER, counts)


def stats_calculating(page, start_day, days):
    visit_counter = 0

    for day_counter in range(0, days + 1):
        day = str(start_day - datetime.timedelta(days=day_counter))
        if day in page:
            visit_counter += page[day]

    return visit_counter