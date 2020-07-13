from django.http import HttpResponse

from pages.stats import visits_counter
from utils.file_utils import get_content
from path import MY_PROJECTS_PAGE, PROJECTS_CSS


def get_projects_page(request):
    visits_counter(request.path)
    file_name = MY_PROJECTS_PAGE
    content = get_content(file_name)
    return HttpResponse(content)

def get_projects_css(request):
    with (PROJECTS_CSS).open("r") as css:
        css = css.read()
    return HttpResponse(css,content_type="text/css")