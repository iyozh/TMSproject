import datetime

from django.http import HttpResponse, request
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from utils.stats_utils import visits_counter


# def get_page_goodbye(request):
#     visits_counter(request.path)
#     hour = datetime.datetime.now().hour
#
#     msg = "day" if hour in range(6, 24) else "night"
#
#     ctx = {
#         "msg":msg
#     }
#
#     return render(request,"goodbye/index.html", ctx)


class GoodbyeView(TemplateView):
    template_name = "goodbye/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        hour = datetime.datetime.now().hour

        msg = "day" if hour in range(6, 24) else "night"

        ctx.update({
        "msg":msg
    })
        return ctx
