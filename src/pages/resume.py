from django.http import HttpResponse

from django.conf import settings

from utils.file_utils import get_content


def get_portfolio(request):
    file_name = settings.PORTFOLIO / "aboutme" / "index.html"
    content = get_content(file_name)
    return HttpResponse(content)


def get_resume_css(request):
    with (settings.PORTFOLIO / "aboutme" / "css" / "main.css").open("r") as css:
        css = css.read()
    return HttpResponse(css,content_type="text/css")