import datetime

from django.template.response import TemplateResponse

from applications.stats.models import Stats


def visits_counter(request, code, content_length):
    one_kb = 2 ** 10
    size = content_length / one_kb
    today = datetime.datetime.now()
    name = ""
    if "name" in request.session:
        name = request.session["name"]
    visit = Stats(
        url=request.path,
        date=today,
        method=request.method,
        user=name,
        code=code,
        size=size,
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
            status_code = 500
            content_length = 0
            try:
                response = super().dispatch(*args, **kwargs)
                status_code = response.status_code
                if isinstance(response, TemplateResponse):
                    response.render()
                content_length = len(bytes(response))
                return response
            finally:
                visits_counter(self.request, status_code, content_length)

    return ViewWithStats
