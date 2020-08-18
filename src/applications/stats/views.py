import datetime

from django import forms
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, RedirectView, TemplateView

from applications.stats.models import Stats
from utils.stats_utils import count_stats


CHOICES = [('ALL', 'ALL'),
           ('GET','GET'),
           ('POST','POST')]

class RadioButtons(forms.Form):
    filtration = forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect,required=False)




@count_stats
class StatsView(ListView):
    template_name = "stats/index.html"
    model = Stats


    def get_queryset(self):
        qs = Stats.objects.all()

        for k,v in self.request.GET.items():
            if v == "ALL":
                return qs
            else:
                qs = qs.filter(method=v.upper())

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        stats = Stats.objects.all()
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = RadioButtons(self.request.GET)
        today = datetime.datetime.now()
        error_code = Q(code__startswith=4 or 5)
        m5 = stats.filter(Q(date__gte=today - datetime.timedelta(minutes=5)) & error_code).count()
        hour = stats.filter(Q(date__gte=today - datetime.timedelta(hours=1)) & error_code).count()
        day = stats.filter(Q(date__gte=today - datetime.timedelta(days=1)) & error_code).count()
        week = stats.filter(Q(date__gte=today - datetime.timedelta(days=7)) & error_code).count()
        ctx.update({"m5":m5,"hour":hour,"day":day,"week":week})
        return ctx


class Reset(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        Stats.objects.all().delete()

        return reverse_lazy("stats:statistic")

