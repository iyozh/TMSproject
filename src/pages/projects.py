from django.http import HttpResponse

from utils.file_utils import get_content
from django.conf import settings




def get_projects_page(request):
    file_name = settings.PORTFOLIO / "projects" / "index.html"
    content = get_content(file_name)
    return HttpResponse(content)

def get_projects_css(request):
    with (settings.PORTFOLIO / "projects" / "css" / "main.css").open("r") as css:
        css = css.read()
    return HttpResponse(css,content_type="text/css")