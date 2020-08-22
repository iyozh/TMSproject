from django.http import HttpResponse

from path import MY_PROJECTS_PAGE
from utils.file_utils import get_content
from utils.stats_utils import visits_counter


def get_projects_page(request):
    visits_counter(request.path)
    file_name = MY_PROJECTS_PAGE
    content = get_content(file_name)
    return HttpResponse(content)
