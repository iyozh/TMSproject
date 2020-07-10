from src.errors import Missing_Data
from src.file_utils import get_content
from src.json_utils import get_json, save_data
from src.path import PORTFOLIO, PROJECTS, PROJECTS_INDEX, PROJECTS_TEMPLATE
from src.responses import respond_200, respond_302
from src.session_utils import parse_user_sessions
from src.stats import visits_counter


def projects_handler(server, method, path):
    switcher = {
        "get": projects_GETresponse,
        "post": projects_editing_handler,
    }
    switcher = switcher[method]

    switcher(server, path)


def projects_editing_handler(server, path):
    switcher = {
        "/test_projects/editing/add": add_project,
        "/test_projects/editing/delete": delete_project,
        "/test_projects/editing/change": change_project,
    }

    handler = switcher[path]
    handler(server)


def projects_GETresponse(server, path):
    visits_counter(path)
    projects_content = get_json(PROJECTS)
    template = get_content(PROJECTS_TEMPLATE)
    projects = ""

    for project in projects_content:
        projects += template.format(
            project_name=projects_content[project]["project_name"],
            project_id=project,
            project_date=projects_content[project]["project_date"],
            project_description=projects_content[project]["project_description"],
        )

    page_content = get_content(PROJECTS_INDEX).format(projects=projects)
    respond_200(server, page_content, "text/html")


def get_editing_page(server, method, path):
    visits_counter(path)
    edit_page = get_content(PORTFOLIO / "test_projects" / "edit_projects.html")
    respond_200(server, edit_page, "text/html")


def add_project(server):
    form_content = parse_user_sessions(server)

    if (
        "project_name" not in form_content
        or "project_id" not in form_content
        or "project_description" not in form_content
        or "project_date" not in form_content
    ):
        raise Missing_Data()

    projects = get_json(PROJECTS)

    new_project = {}

    id_new_project = form_content["project_id"]

    if id_new_project in projects:
        raise Missing_Data()

    new_project[id_new_project] = {
        "project_name": "",
        "project_description": "",
        "project_date": "",
    }

    for item in form_content:
        if item in new_project[id_new_project]:
            new_project[id_new_project][item] = form_content[item]

    projects.update(new_project)

    save_data(PROJECTS, projects)

    respond_302(server, "/test_projects", "")


def delete_project(server):
    form = parse_user_sessions(server)
    projects = get_json(PROJECTS)

    if "project_id" not in form:
        raise Missing_Data()

    project_id = form["project_id"]

    if project_id not in projects:
        raise Missing_Data()

    projects.pop(project_id)
    save_data(PROJECTS, projects)
    respond_302(server, "/test_projects", "")


def change_project(self):
    form = parse_user_sessions(self)
    projects = get_json(PROJECTS)

    if "project_id" not in form:
        raise Missing_Data()

    for item in form:
        if item != "project_id":
            projects[form["project_id"]][item] = form[item]

    save_data(PROJECTS, projects)
    respond_302(self, "/test_projects", "")
