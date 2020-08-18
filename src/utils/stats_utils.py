import datetime

from django.utils import timezone

from applications.stats.models import Stats


def visits_counter(request, code):
    today = datetime.datetime.now()
    name = ""
    if "name" in request.session:
        name = request.session["name"]
    visit = Stats(
        url=request.path, date=today, method=request.method, user=name, code=code
    )
    visit.save()


def stats_calculating(page, start_day, days):
    visit_counter = 0

    for day_counter in range(0, days + 1):
        day = str(start_day - datetime.timedelta(days=day_counter))
        if day in page:
            visit_counter += page[day]

    return visit_counter


def count_stats(view):
    class ViewWithStats(view):
        def dispatch(self, *args, **kwargs):
            try:
                response = super().dispatch(*args, **kwargs)
                return response
            finally:
                visits_counter(self.request, response.status_code)

    return ViewWithStats
