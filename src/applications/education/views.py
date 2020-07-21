from django.shortcuts import render
from django.views.generic.base import View

from path import EDUCATION
from utils.json_utils import get_json
from utils.stats_utils import visits_counter
from utils.theme_utils import change_mode, get_theme


class EducationView(View):
    def get(self, request, **kwargs):
        visits_counter(request.path)
        theme = get_theme(request)
        edu_info = get_json(EDUCATION)
        ctx = {"theme": theme, "edu_info": edu_info}
        return render(request, "education/index.html", ctx)

    def post(self, request):
        return change_mode(request, "/education")
