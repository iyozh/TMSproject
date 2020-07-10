from src.utils.file_utils import get_content
from src.path import PORTFOLIO
from src.responses import respond_200
from src.pages.stats import visits_counter


def get_projects(server, method, path):
    visits_counter(path)
    file_name = PORTFOLIO / "projects" / "index.html"
    content = get_content(file_name)
    respond_200(server, content, "text/html")
