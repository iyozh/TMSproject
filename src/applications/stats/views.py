from django import forms
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, TemplateView

from applications.stats.models import Stats
from utils.stats_utils import count_stats


class CheckBoxFilter(forms.Form):
    all = forms.BooleanField(required=False)
    get = forms.BooleanField(required=False)
    post = forms.BooleanField(required=False)


@count_stats
class StatsView(FormView):
    template_name = "stats/index.html"
    model = Stats
    form_class = CheckBoxFilter
    success_url = reverse_lazy("stats:statistic")

    def get_context_data(self, **kwargs):

        ctx = super().get_context_data(**kwargs)

        stats = Stats.objects.all().reverse()

        ctx.update({"stats": stats})

        return ctx

    def form_valid(self, form):
        content = form.cleaned_data
        dct = {
            "all": Stats.objects.all(),
            "get": Stats.objects.filter(method="GET"),
            "post": Stats.objects.filter(method="POST"),
        }
        choice = None
        for k, v in content.items():
            if v is True:
                choice = dct[k]

        return super().form_valid(form)


class Reset(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        Stats.objects.all().delete()

        return reverse_lazy("stats:statistic")
