from django.http import HttpResponse

from src.path import PORTFOLIO
from src.utils.utils import get_content


def get_portfolio(request):
    file_name = PORTFOLIO / "aboutme" / "index.html"
    content = get_content(file_name)
    return HttpResponse(content)