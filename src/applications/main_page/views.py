from django.views.generic import TemplateView

from utils.stats_utils import visits_counter
from utils.theme_utils import change_mode, get_theme


class MainPageView(TemplateView):
    template_name = "main_page/index.html"

    def dispatch(self, request, *args, **kwargs):
        visits_counter(self.request.path)
        return super().dispatch(request)

    def post(self, request):
        return change_mode(request, "/")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        theme = get_theme(self.request)
        ctx.update({"theme": theme})

        return ctx
