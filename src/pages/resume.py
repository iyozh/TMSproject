from django.http import HttpResponse

from path import RESUME_INDEX
from utils.file_utils import get_content
from utils.stats_utils import visits_counter


def get_portfolio(request):
    visits_counter(request.path)
    file_name = RESUME_INDEX
    content = get_content(file_name)
    return HttpResponse(content)
