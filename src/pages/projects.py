from django.http import HttpResponse

from src.utils.file_utils import get_content
from src.path import PORTFOLIO




def get_projects_page(request):
    file_name = PORTFOLIO / "projects" / "index.html"
    content = get_content(file_name)
    return HttpResponse(content)