from django.http import HttpResponse

from pages.stats import visits_counter
from path import RESUME_CSS, RESUME_INDEX

from utils.file_utils import get_content


def get_portfolio(request):
    visits_counter(request.path)
    file_name = RESUME_INDEX
    content = get_content(file_name)
    return HttpResponse(content)


def get_resume_css(request):
    with (RESUME_CSS).open("r") as css:
        css = css.read()
    return HttpResponse(css,content_type="text/css")