from django.views.generic.base import TemplateView

from path import EDUCATION
from utils.json_utils import get_json
from utils.stats_utils import count_stats


@count_stats
class EducationView(TemplateView):
    template_name = "education/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        edu_info = get_json(EDUCATION)
        ctx.update({"edu_info": edu_info})

        return ctx
