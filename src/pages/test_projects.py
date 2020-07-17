import os

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods

from errors import Missing_Data
from utils.file_utils import get_content
from utils.json_utils import get_json, save_data
from path import PORTFOLIO, PROJECTS, PROJECTS_INDEX, PROJECTS_TEMPLATE
from utils.session_utils import parse_user_sessions
from pages.stats import visits_counter

@require_http_methods(['GET', 'POST'])
def projects_handler(request,**kw):
    switcher = {
        "GET": projects_GETresponse,
        "POST": projects_editing_handler,
    }
    handler = switcher[request.method]

    try:
        return handler(request,"/test_projects",kw)
    except Missing_Data:
        return HttpResponse("You miss something...")


def projects_editing_handler(request, redirect,kw):
    project_id = kw.get("project_id",0)
    switcher = {
        "/test_projects/editing/add": add_project,
        f"/test_projects/id/{project_id}/delete": delete_project,
        f"/test_projects/id/{project_id}/editing/edit/": edit_project,
    }

    handler = switcher[request.path]
    return handler(request, redirect,kw)


def projects_GETresponse(request,redirect,kw):
    visits_counter(request.path)
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
    return HttpResponse(page_content, "text/html")


def get_certain_project(request, **kw):
    visits_counter(request.path)
    project_id = kw["project_id"]
    projects = get_json(PROJECTS)

    certain_project  = projects[project_id]

    edit_page = get_content(PORTFOLIO / "test_projects" / "c_project.html").format(**certain_project,project_id=project_id)
    return HttpResponse(edit_page, "text/html")


def add_project(request,redirect,kw):
    form_content = parse_user_sessions(request)

    if (
        "project_name" not in form_content
        or "project_description" not in form_content
        or "project_date" not in form_content
    ):
        raise Missing_Data()

    projects = get_json(PROJECTS)

    new_project = {}

    id_new_project = os.urandom(16).hex()

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

    return HttpResponseRedirect(redirect)


def delete_project(request,redirect,kw):
    project_id = kw['project_id']
    projects = get_json(PROJECTS)
    projects.pop(project_id)
    save_data(PROJECTS,projects)
    return HttpResponseRedirect(redirect)


def edit_project(request,redirect,kw):
    form = parse_user_sessions(request)
    projects = get_json(PROJECTS)

    # if "project_id" not in form:
    #     raise Missing_Data()

    project_id = kw["project_id"]
    for item in form:
        projects[project_id][item] = form[item]

    save_data(PROJECTS, projects)
    return HttpResponseRedirect(redirect)


def get_adding_page(request):
    adding_page = get_content(PORTFOLIO / "test_projects" / "add_projects.html")
    return HttpResponse(adding_page)

def get_editing_page(request,**kw):
    project_id = kw["project_id"]
    projects = get_json(PROJECTS)
    certain_project = projects[project_id]
    editing_page = get_content(PORTFOLIO / "test_projects" / "edit_projects.html").format(**certain_project,project_id=project_id)
    return HttpResponse(editing_page)