import datetime

from django.views.generic import TemplateView


class GoodbyeView(TemplateView):
    template_name = "goodbye/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        hour = datetime.datetime.now().hour

        msg = "day" if hour in range(6, 24) else "night"

        ctx.update({"msg": msg})
        return ctx
