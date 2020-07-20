import datetime
from path import COUNTER
from utils.json_utils import get_json, save_data


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