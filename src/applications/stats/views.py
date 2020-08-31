from django import forms
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView

from applications.stats.models import Stats
from utils.stats_utils import count_stats

CHOICES = [("ALL", "ALL"), ("GET", "GET"), ("POST", "POST")]


class RadioButtons(forms.Form):
    filtration = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect, required=False
    )


@count_stats
class StatsView(ListView):
    template_name = "stats/index.html"
    model = Stats

    def get_queryset(self):
        qs = Stats.objects.all()

        for k, v in self.request.GET.items():
            qs = Stats.objects.all() if v == "ALL" else qs.filter(method=v.upper())

        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = RadioButtons(self.request.GET)
        ctx["dashboard"] = Stats.generate_dashboard()
        return ctx


class Reset(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        Stats.objects.all().delete()

        return reverse_lazy("stats:statistic")
