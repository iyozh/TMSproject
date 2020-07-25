import datetime

from django.views.generic import TemplateView

from utils.stats_utils import visits_counter
from utils.theme_utils import change_mode, get_theme


class GoodbyeView(TemplateView):
    template_name = "goodbye/index.html"

    def dispatch(self, request, *args, **kwargs):
        visits_counter(self.request.path)
        return super().dispatch(request)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        theme = get_theme(self.request)
        hour = datetime.datetime.now().hour

        msg = "day" if hour in range(6, 24) else "night"

        ctx.update({"msg": msg, "theme": theme})
        return ctx

    def post(self, request):
        return change_mode(request, "/goodbye")
